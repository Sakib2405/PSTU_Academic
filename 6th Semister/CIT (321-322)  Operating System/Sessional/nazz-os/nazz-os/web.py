from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import sys
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")


@app.get("/")
async def index():
    with open("web/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    loop = asyncio.get_event_loop()

    # Prefer POSIX PTY+fork where available (Linux/WSL). On Windows fall back to
    # launching `main.py` as a subprocess and proxying stdin/stdout.
    use_pty = hasattr(os, "fork") and hasattr(os, "openpty")

    if use_pty:
        master_fd, slave_fd = os.openpty()

        pid = os.fork()
        if pid == 0:
            # Child: attach slave pty to stdio and exec the app
            os.setsid()
            os.dup2(slave_fd, 0)
            os.dup2(slave_fd, 1)
            os.dup2(slave_fd, 2)
            os.close(master_fd)
            os.close(slave_fd)
            os.execv(sys.executable, [sys.executable, "main.py"])
            return

        # Parent: close slave fd, communicate with master_fd
        os.close(slave_fd)

        async def read_from_pty():
            try:
                while True:
                    data = await loop.run_in_executor(None, os.read, master_fd, 1024)
                    if not data:
                        break
                    try:
                        await websocket.send_text(data.decode(errors="ignore"))
                    except Exception:
                        break
            finally:
                try:
                    await websocket.close()
                except Exception:
                    pass

        reader_task = asyncio.create_task(read_from_pty())

        try:
            while True:
                msg = await websocket.receive_text()
                # Write input to the PTY master
                os.write(master_fd, msg.encode())
        except Exception:
            pass
        finally:
            reader_task.cancel()
            try:
                os.close(master_fd)
            except Exception:
                pass
    else:
        # Windows / non-POSIX fallback: use an asyncio subprocess
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "main.py",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        async def read_stream(stream):
            try:
                while True:
                    data = await stream.read(1024)
                    if not data:
                        break
                    try:
                        await websocket.send_text(data.decode(errors="ignore"))
                    except Exception:
                        break
            finally:
                try:
                    await websocket.close()
                except Exception:
                    pass

        reader_task = asyncio.create_task(read_stream(proc.stdout))

        try:
            while True:
                msg = await websocket.receive_text()
                if proc.stdin:
                    proc.stdin.write(msg.encode())
                    await proc.stdin.drain()
        except Exception:
            pass
        finally:
            reader_task.cancel()
            try:
                if proc.returncode is None:
                    proc.kill()
            except Exception:
                pass


if __name__ == "__main__":
    # Run the FastAPI app with Uvicorn when executed directly.
    # Install with: pip install uvicorn fastapi
    try:
        import uvicorn

        uvicorn.run("web:app", host="0.0.0.0", port=8000)
    except Exception as exc:
        print("Failed to start server. Ensure 'uvicorn' is installed.")
        raise

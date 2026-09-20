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

    # Open a new PTY and fork the child to run the TUI app
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

    loop = asyncio.get_event_loop()

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

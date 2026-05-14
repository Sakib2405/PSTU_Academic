import wave
import struct
import math
import cv2
import numpy as np

# -----------------------------
# Generate a 5-second audio.wav
# -----------------------------
sample_rate = 44100
duration = 5
frequency = 440  # A4 note

with wave.open('audio.wav', 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    
    for i in range(sample_rate * duration):
        value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
        data = struct.pack('<h', value)
        wav_file.writeframes(data)

print("audio.wav created (5 seconds, 440Hz tone)")


# -----------------------------
# Generate a 5-second video.mp4
# -----------------------------
width, height = 640, 480
fps = 30
duration = 5
total_frames = fps * duration

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('video.mp4', fourcc, fps, (width, height))

for i in range(total_frames):
    
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    
    color = (i % 255, (i * 2) % 255, (i * 3) % 255)
    cv2.rectangle(frame, (0, 0), (width, height), color, -1)
    
    
    text_pos = (50 + (i % 300), 240)
    cv2.putText(frame, "Sample Video", text_pos,
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)

    video.write(frame)

video.release()
print("video.mp4 created (5 seconds, 30 FPS, colored animation)")

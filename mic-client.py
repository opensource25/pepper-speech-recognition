import pyaudio
import socket

# Audio Settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Socket Settings
HOST = '127.0.0.1'
PORT = 5001

p = pyaudio.PyAudio()
with p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK) as stream:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print("streaming audio...")

    try:
        while True:
            data = stream.read(CHUNK)
            s.send(data)
    except KeyboardInterrupt:
        s.close()

print("stop streaming ...")

p.terminate()

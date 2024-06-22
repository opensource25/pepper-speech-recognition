import pyaudio
import socket

# Audio Settings - (need to be the same for client and host)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

MIC_DEVICE_INDEX = None  # None for default device

# Socket Settings
HOST = '127.0.0.1'  # The server's IP address
PORT = 5001

# setup socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# setup audio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# start streaming audio to recognition-host.py
print("streaming audio...")

try:
    while True:
        data = stream.read(CHUNK)
        print(data)
        s.send(data)
except KeyboardInterrupt:
    pass

# stop streaming audio
print("stop streaming ...")

stream.stop_stream()
stream.close()
audio.terminate()
s.close()

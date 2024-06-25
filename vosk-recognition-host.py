import socket
import pyaudio
from vosk import Model, KaldiRecognizer
# import wave

# Audio Settings - (need to be the same for client and host)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Socket Settings
HOST = ''  # leave empty to accept connections from any IP address or put client IP address here
PORT = 5001

# setup socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print("Connected by", addr)

# setup audio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# receive audio from mic-client
print("receiving audio...")

# frames = []  # save audio frames to write audio to audiofile for testing purposes

# setup vosk speech recognition
model = Model("./models/vosk-model-de-0.21") # path to the model folder
recognizer = KaldiRecognizer(model, RATE)

try:
    while True:
        data = conn.recv(CHUNK)
        if not data:
            break
        # frames.append(data)

        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            print(text)

except KeyboardInterrupt:
    pass

# stop receiving
print("stop receiving audio")
stream.stop_stream()
stream.close()
audio.terminate()
conn.close()
s.close()

# write audio to file for testing purposes
# waveFile = wave.open("test.wav", 'wb')
# waveFile.setnchannels(CHANNELS)
# waveFile.setsampwidth(audio.get_sample_size(FORMAT))
# waveFile.setframerate(RATE)
# waveFile.writeframes(b''.join(frames))
# waveFile.close()

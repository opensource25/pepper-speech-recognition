import socket
import pyaudio
# from whisper_mic import WhisperMic
import whisper
import numpy as np
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

# receive audio from mic-client
print("receiving audio...")

# frames = []  # save audio frames to write audio to audiofile for testing purposes

# setup speech recognition
model = whisper.load_model("base")

try:
    while True:
        data = conn.recv(CHUNK)
        if not data:
            break
        # frames.append(data)

        audio_data = np.frombuffer(data, dtype=np.int16).flatten().astype(np.float32)

        text = model.transcribe(audio_data)
        print(text)

except KeyboardInterrupt:
    pass

# stop receiving
print("stop receiving audio")
conn.close()
s.close()

# write audio to file for testing purposes
# waveFile = wave.open("test.wav", 'wb')
# waveFile.setnchannels(CHANNELS)
# waveFile.setsampwidth(audio.get_sample_size(FORMAT))
# waveFile.setframerate(RATE)
# waveFile.writeframes(b''.join(frames))
# waveFile.close()

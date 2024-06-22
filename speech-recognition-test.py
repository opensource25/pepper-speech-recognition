import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

try:
    print("Vosk thinks you said " + r.recognize_vosk(audio))
except sr.UnknownValueError:
    print("Vosk could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Vosk; {e}")
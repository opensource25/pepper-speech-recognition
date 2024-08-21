This is a set of scripts designed to send microphone audio from a low performance computer, but with a microphone to a high performance computer or server for running speech recognition there and send the results to another component.
   
The project is coded as a workaround to get a local, good and especially fast speech recognition for the humanoid robot pepper.
For this the client scripts need to be Python 2 compatible.  
For the python 2 compatibility you need to use pyaudio version 0.2.11 as it is the last version of pyaudio to support python2.
Sadly I wasn't able to install pyaudio on pepper, so I build an other mic client version with the naoqi functions, but the quality sadly isn't the best.

The vosk based Version works perfectly fine, but the whisper version is for now just some unsuccessful trying around. The speech-recognition-test.py file was just a first test playing a bit with a possible module for the speech recognition, but I went another way, but it may still help somebody.

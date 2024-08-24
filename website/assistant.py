from flask import Flask, render_template, jsonify, request
from IPython.display import clear_output
import numpy as np
import threading
import datetime
import pyaudio
import logging
import struct
import torch
import time
import os

from py_programs.voice_comparison import detect_speech, verify_speech, load_speaker_embeddings
from py_programs.audio_processing import create_spect, reset_audio, save
from py_programs.speech_recognition import speech_recognition
from py_programs.respond import respond


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def index():
    return render_template('index.html')


class SpeechRecognitionApp:
    def __init__(self):
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.fs = 16000
        self.seconds = 10
        self.filename = "temp.wav"
        self.frames = []

        self.n_mels = 128
        self.win_length = 160
        self.hop_length = 80
        self.max_length = 8000

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk,
                                  input=True)

        if os.path.exists(self.filename):
            os.remove(self.filename)

        self.desired_seconds = None
        self.desired_time = (-1, -1)
        self.prev_seconds = None

        self.speaking_history = []

        self.counter = 0
        self.periodically_check = False
        self.speakers, self.speaker_embeddings = load_speaker_embeddings()
        self.beam_search_result = "..."
        self.response = "..."
        self.original_response = np.array("...")
        self.motion = ""
        self.waveform = []
        self.stopped = False

    def recognize_speech(self):
        while True:
            if not self.stopped:
                if len(self.frames) > self.seconds * self.fs / self.chunk:
                    for i in range(int(len(self.frames) - (self.seconds * self.fs / self.chunk))):
                        self.frames.pop(0)

                data = self.stream.read(self.chunk, exception_on_overflow=False)
                self.frames.append(data)


                num_samples = len(data) // 2  # Each sample is 2 bytes (16 bits)
                format = f"{num_samples}h"  # 'h' is the format for 16-bit signed integers
                samples = struct.unpack(format, data)

                samples = np.array(samples)
                self.waveform = (samples / 32768.0).tolist()


                save(self.frames)
                if self.counter % 5 == 0:
                    waveform, padded_wav, spect = create_spect(self.filename, self.max_length, 8000,
                                                            self.n_mels, self.win_length, self.hop_length) # Get last second

                    # Check if still speaking
                    if self.periodically_check:
                        self.speech_detected = detect_speech(spect.to("cuda"))
                        if  self.speech_detected <= 0.8:
                            self.periodically_check = False
                            print("End of speaking")

                            # Automatic Speech Recognition
                            self.beam_search_result = speech_recognition(waveform)

                            # Speaker identification
                            #classifications = []
                            #for embedding in self.speaker_embeddings:
                            #    classifications.append(verify_speech(embedding.to("cuda"), self.filename)[0][0])
 
                            #print(classifications)
                            #if np.max(classifications) >= .8:
                            #    print(f"{self.speakers[np.argmax(classifications)][:-3]} speaking")
                            #else:
                            #    print("Other speaking")
                                
                            print("Input: ", self.beam_search_result)
                            self.original_response, self.response, self.desired_seconds, self.desired_time, self.motion = respond("user: " + self.beam_search_result + " jarvis:")
                            print("Response: ", self.response.split("jarvis: ")[-1])

                            # If a timer is created, set a timestamp
                            if self.desired_seconds != None:
                                self.prev_seconds = time.time()

                            self.speaking_history.append({"User": self.beam_search_result, "Jarvis": self.original_response.tolist().split("jarvis: ")[-1]})

                            if self.original_response.tolist().split("jarvis: ")[-1].strip() != "/t":
                                time.sleep(1)
                                self.frames, speaking_counter = reset_audio(self.filename)
                            else:
                                self.frames, speaking_counter = reset_audio(self.filename, sleep=False)
                            
                            self.response = "..."
                            self.beam_search_result = "..."
                            self.motion = ""
                            
                            # Search for the speakers name
            #                 elif np.max(classifications) >= .8 and np.argmax(classifications) != 0:
            #                     speaking_history.append({speakers[np.argmax(classifications)]: self.beam_search_result, "Jarvis": self.response})
            #                 else:
            #                     speaking_history.append({"Random": self.beam_search_result, "Jarvis": ""})
                    ######## First detect my voice
                    
                    # Speaking detected
                    self.speech_detected = detect_speech(spect.to("cuda"))
                    
                    if not self.periodically_check and padded_wav.shape[1] <= waveform.shape[1] and self.speech_detected >= .9:
                        # My voice talking
                        print("Speaking detected")
                        self.periodically_check = True

                    #print(self.speech_detected)
                    #clear_output(wait=True)

                self.counter += 1

                ################ Reminder + timer ################
                if self.desired_seconds != None and round(time.time() - self.prev_seconds) == self.desired_seconds:
                    # playsound("timer")
                    print("Timer ended")
                hours, minutes = datetime.datetime.now().strftime("%I:%M").split(":")
                if self.desired_time[0] == int(hours) and self.desired_time[1] == int(minutes):
                    print("Reminder")
                    self.desired_time = (-1, -1)

speech_app = SpeechRecognitionApp()

# Start the speech recognition in a separate thread
recognition_thread = threading.Thread(target=speech_app.recognize_speech)
recognition_thread.daemon = True
recognition_thread.start()

@app.route('/speech', methods=['POST'])
def get_speech_text():
    data = request.json
    stop = data.get('stop')
    if stop:
        speech_app.stopped = True
    else:
        speech_app.stopped = False

    original = speech_app.original_response.tolist().split("jarvis: ")[-1].replace("/t", "")
    response = speech_app.response.split("jarvis: ")[-1].replace("/t", "")
    detection = round(speech_app.speech_detected.to("cpu").item(), 3)
    return jsonify({'output': original, 'speech': speech_app.beam_search_result, 'response': response, 'detection': detection, 'motion': speech_app.motion, 'waveform': speech_app.waveform})

if __name__ == '__main__':
    app.run(debug=False)
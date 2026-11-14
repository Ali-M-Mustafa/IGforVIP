#Import necessary Libraries
import speech_recognition as SRG
import time

#Import Code Files
from play import play
store = SRG.Recognizer() # create a recognizer 

def get_txt() :
    with SRG.Microphone() as s:
        print("speak...")
        audio_input = store.record(s, duration=2) #record audio
        try:
            text_output = store.recognize_google(audio_input) #convert speech to text
            print(text_output)
            return text_output
        except:
            print("Could not process the audio input.")
            return None #in case not recognized 
        
#this function compares the text with the names of the identified moods
def listen():
    play("hi user")
    while True :
        text_output = get_txt()
        
        if text_output is None:
            play('sorry')   
        elif 'face' in text_output:
            return 'face'
            break
        elif 'recognition' in text_output:
            return 'face'
            break
        elif 'vibration' in text_output:
            return 'vibration'
            break
        elif 'object' in text_output:
            return 'object'
            break
        elif 'detection' in text_output:
            return 'object'
            break
        else:
           play('sorry')
   
#print(listen ())

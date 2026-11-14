#this code plays audio file from a path             
from pygame import mixer
mixer.init()

def play(sound) :
    mixer.music.load("voices/{}".format(sound))
    mixer.music.play()
    while mixer.music.get_busy() == True: pass # keep the program waiting while playing the file
        

#play('')

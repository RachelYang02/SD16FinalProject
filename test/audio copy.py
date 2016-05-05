import alsaaudio
import audioop
import pygame


inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,0)
inp.setchannels(1)
inp.setrate(16000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)

while True:
        l,data = inp.read()
        if l:
            d = audioop.rms(data,2)
            print d

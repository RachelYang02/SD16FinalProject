import alsaaudio
import audioop
import time
import pygame

class Audio(object):
	"""Collects audio data and returns volume continuously"""

	def __init__(self,rate = 16000, periodSize = 160):

		# rate is the sample rate. default 16kHz. Period size. idk what that is...
		self.rate, self.periodSize = rate, periodSize

		# creates the input channel from the mic 
		self.input = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,0)
		self.input.setchannels(1)
		self.input.setrate(self.rate)
		self.input.setformat(alsaaudio.PCM_FORMAT_S16_LE)
		self.input.setperiodsize(self.periodSize)

		self.currentVol = 0

	
	def collectAudio(self):
		# continuously collects audio data and returns volume every 0.1 seconds
		while 1:

			# so maybe this is less computationally demanding???? We just don't
			# need it to run that much

			# reads two things from the audio stream. l is length, d is captured data
			l,data = self.input.read()

			# if l is 0, we have no audio data
			if l:
				# root mean sqaure so negatives won't matter!
				# this is pretty typical for intensity analysis
				self.currentVol = audioop.rms(data,2)
			#print self.currentVol

if __name__ == '__main__':

	stream = Audio()
	stream.collectAudio()

import numpy as np 
import pyaudio
from array import array
import matplotlib.pyplot as mplib 

# converts a string into a numpy array of bits
# each character is 7 bits???
def string2NPArray(s):
	bits = np.array([])
	for a in bytearray(s,'ascii'):
		for b in range(0,7):
			bits = np.append(bits,float((a>>(7-b-1)&1)))
	return bits



# get samples from the mic

def getAudio(sampleRate = 8000, threshold = 1000, chunkSize = 1000):
	# creates the pyaudio object to start getting audio
	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paInt16, channels=1, rate=sampleRate,input=True, output=False, framesPerBuffer=chunk_size)

	# storage numpy array for our audio!
	dataStorage  = array('h')

	# function to check that our noise is above a certain level
	def quiet(soundData,thresh):
		return max(soundData) < thresh

	# makes sure we aren't taking in no sound
	while 1:
		#reads a bit of audio data 
		sound = stream.ready(chunkSize)
		#converts our sound data into a numpy array
		data = array('h',sound)

		# makes sure we didn't just get a bunch of noooothing
		if quiet(data,threshold):
			break

	# convert to a numpy array?
	x = np.frombuffer(dataStorage, dtype= np.dtype('int16'))   

	# close our audio stream
	stream.stop_stream()
	stream.close()
	p.terminate 

if __name__ == '__main__':
	getAudio()

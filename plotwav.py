from pylab import *
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy

sampFreq, snd = wavfile.read('1over.wav')
s1 = snd[:,0]

timeWindow = 5
duration = s1.size/sampFreq
duration = duration / timeWindow
s1 = [val* -1 if val<0 else val for val in s1]

plotFreq = 1
sampFreq = sampFreq/plotFreq
sampFreq = sampFreq * timeWindow
mediaSamp = []
meanSamp = []
modeSamp = []

for x in range(0, duration * plotFreq):
	# modeSamp.append(stats.mode(s1[x*sampFreq +1: (x+1)*sampFreq]))
	mediaSamp.append(numpy.median(s1[x*sampFreq +1: (x+1)*sampFreq]))
	meanSamp.append(numpy.mean(s1[x*sampFreq +1: (x+1)*sampFreq]))

# print mediaSamp
print len(mediaSamp)

# plot mean samples
timeArray = arange(0, duration, 1./plotFreq)
# plt.subplot(2,1,1)
plt.plot(timeArray, mediaSamp)
plt.xlabel('time')
plt.ylabel('amplitude ' + str(numpy.mean(s1)))

# plot mean
wholeMean = numpy.mean(meanSamp)
meanY = [wholeMean for i in range(0, duration)]
meanX = [i for i in range(0, duration) ]
plt.plot(meanX, meanY, label = 'mean')

#plot median
wholeMedian = numpy.median(mediaSamp)
medianY = [wholeMedian for i in range(0, duration)]
medianX = [i for i in range(0, duration)]
plt.plot(medianX, medianY, label = 'median')
'''
#plot mode
wholeMode = stats.mode(modeSamp)
modeY = [wholeMode for i in range(0, duration)]
modeX = [i for i in range(0, duration)]
plt.plot(modeX, modeY, label = 'mode')
'''

'''
plt.subplot(2,1,2)
plt.plot(timeArray, meanSamp)
plt.xlabel('time /100 ')
plt.ylabel('amplitude')
'''
plt.legend()
plt.show()


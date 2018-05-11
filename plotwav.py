from pylab import *
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy
from collections import OrderedDict
import copy
from video_utilites import get_video_from_time_frames, get_audio_from_video
from optparse import OptionParser



def main(path_to_video):
	path_to_audio = 'audio_file.wav'

	get_audio_from_video(path_to_video, path_to_audio)
	sampFreq, snd = wavfile.read(path_to_audio)
	s1 = snd[:,0]

	windowTime = 4
	audioLength = s1.size/sampFreq
	print "audio length: " + str(audioLength)
	windows = audioLength / windowTime
	print "windows: " + str(windows)
	s1 = [val* -1 if val<0 else val for val in s1]

	plotFreq = 1
	sampFreq = (sampFreq * windowTime) / plotFreq
	medianSamp = []
	meanSamp = []
	modeSamp = []
	areaAboveMean = OrderedDict()

	for x in range(0, windows * plotFreq):
		# modeSamp.append(stats.mode(s1[x*sampFreq +1: (x+1)*sampFreq]))
		medianSamp.append(numpy.median(s1[x*sampFreq: (x+1)*sampFreq]))
		meanSamp.append(numpy.mean(s1[x*sampFreq: (x+1)*sampFreq]))

	# print meanSamp
	wholeMean = numpy.mean(meanSamp)
	# print wholeMean
	wholeMedian = numpy.median(medianSamp)

	localArea = 0
	localStartTime = 0
	aboveMean = False
	for x in range(0, len(meanSamp)):
		if meanSamp[x] >= wholeMean:
			if not(aboveMean):
				aboveMean = True
				localStartTime = windowTime * (x)

			localArea = localArea + (meanSamp[x] - wholeMean)

		elif aboveMean:
			areaAboveMean[localStartTime] = [windowTime * (x), localArea]
			localArea = 0
			aboveMean = False

	if not(localStartTime in areaAboveMean):
		areaAboveMean[localStartTime] = [windows * windowTime, localArea]

	print "peaks:"
	print areaAboveMean

	# group peaks movements within cool-off sec
	coolOffTime = 20
	prevStartTime = -1
	prevEndTime = -1
	prevLocalArea = -1
	peakMovements = OrderedDict()
	for key, value in areaAboveMean.iteritems():
		if prevEndTime == -1:
			prevStartTime = key
			prevEndTime = value[0]
			prevLocalArea = value[1]
			peakMovements[key] = [value[0], value[1]]
		elif (key - prevEndTime) < coolOffTime:
			peakMovements[prevStartTime] = [value[0], prevLocalArea + value[1]]
			prevEndTime = value[0]
			prevLocalArea = prevLocalArea + value[1]
		else:
			peakMovements[key] = [value[0], value[1]]
			prevStartTime = key
			prevEndTime = value[0]
			prevLocalArea = value[1]
			
	# print "all-peak-movements:"
	# print peakMovements

	results = list()
	for k, v in peakMovements.iteritems():
		if v[0]-k > 8:
			results.append((k, v[0], v[1]))

	print "peak-movements:"
	print results
	# print len(meanSamp)

	with open('heatmap_{}.csv'.format(path_to_video), 'w') as csv:
		for x,y,z in results:
			csv.write('{},{},{:.2f}'.format(x,y,z)+'\n')

	get_video_from_time_frames(path_to_video, results, 'result.mp4')
	# plot mean samples
	timeArray = arange(1, windows+1, 1./plotFreq)
	timeArray = timeArray * windowTime
	# plt.subplot(2,1,1)
	plt.plot(timeArray, meanSamp)
	plt.xlabel('time')
	plt.ylabel('amplitude ' + "{:.2f}".format(wholeMean))

	# plot mean
	meanY = [wholeMean for i in range(0, audioLength)]
	meanX = [i for i in range(0, audioLength) ]
	plt.plot(meanX, meanY, label = 'mean')

	#plot median
	medianY = [wholeMedian for i in range(0, audioLength)]
	medianX = [i for i in range(0, audioLength)]
	plt.plot(medianX, medianY, label = 'median')

	# '''
	# #plot mode
	# wholeMode = stats.mode(modeSamp)
	# modeY = [wholeMode for i in range(0, windows)]
	# modeX = [i for i in range(0, windows)]
	# plt.plot(modeX, modeY, label = 'mode')
	# '''

	# '''
	# plt.subplot(2,1,2)
	# plt.plot(timeArray, meanSamp)
	# plt.xlabel('time /100 ')
	# plt.ylabel('amplitude')
	# '''

	# for key, value in peakMovements.iteritems():
	# 	X = [(key + i ) for i in range(0, value[0] - key + 1)]
	# 	Y = [wholeMean for i in range(0, value[0] - key + 1)]
	# 	plt.plot(X, Y, color = "black")

	for s,e,_ in results:
		X = [(s + i ) for i in range(0, e - s + 1)]
		Y = [wholeMean for i in range(0, e - s + 1)]
		plt.plot(X, Y, color = "black")

	plt.legend()
	plt.show()

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-v", "--video_file_path", dest="path_to_video", help="path to video file", metavar="FILE")
	(options, args) = parser.parse_args()
	main(options.path_to_video)


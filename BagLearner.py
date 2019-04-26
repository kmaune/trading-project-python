import pandas as pd
import numpy as np
from scipy import stats

class BagLearner(object):

	def __init__(self, learner, kwargs={}, bags = 20, boost = False, verbose = False):
		self.learner = learner
		self.kwargs = kwargs
		self.bags = bags
		self.boost = boost
		self.verbose = verbose
		self.allLearners = [] 
		self.createBagLearner()


	def createBagLearner(self):
		for i in range(self.bags):
			self.allLearners.append(self.learner(**self.kwargs))

	#Given x and y data to build tree with
	def addEvidence(self, dataX, dataY):
		for learner in self.allLearners:
			i = np.random.choice(dataX.shape[0], size = dataX.shape[0])
			x = dataX[i, :]
			y = dataY[i]
			learner.addEvidence(x,y)
			#print learner.decisionTree

	def query(self, points):
		allResults = []
		modeResults = []
		for learner in self.allLearners:
			result =  learner.query(points)
			allResults.append(result)

		allResults = np.asarray(allResults)
		#mean = np.mean(allResults, axis=0)
		for i in range(0, allResults.shape[1]):
			mode = stats.mode(allResults[:, i])
			modeResults.append(mode[0][0])

		modeArray = np.asarray(modeResults)
		#print modeArray

		#print mean.shape
		#print "MEAN: ", mean
		#mean = 10
		#return mean
		return modeArray
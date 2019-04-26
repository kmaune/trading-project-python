import pandas as pd
import numpy as np
from scipy import stats

class RTLearner(object):

	def __init__(self, leaf_size = 1, verbose = False):
		self.leaf_size = leaf_size
		self.verbose = verbose
		self.decisionTree = None

	#Given x and y data to build tree with
	def addEvidence(self, dataX, dataY):
		self.decisionTree = self.build_tree(dataX, dataY)

	def query(self, points):
		dataY = []
		for data in points:
			#print data
			curN = 0;
			currentNode = self.decisionTree[0]
			classified = False;
			#print "ndim: ", self.decisionTree.ndim 
			#print "RT_Tree = ", self.decisionTree
			#print "currentNode: ", currentNode
			if(self.decisionTree.ndim > 1):
				feature = int(currentNode[0])
				splitVal = currentNode[1]
				classified = False
			else:
				dataY.append(self.decisionTree[1])
				classified = True

			while not classified:
				#print "Here"
				if feature == -1:
					dataY.append(splitVal)
					#print "classified"
					classified = True
					continue

				elif data[feature] <= splitVal:
					nextNode = int(currentNode[2])
					currentNode = self.decisionTree[curN + nextNode]
					curN = curN + nextNode;

				else:
					nextNode = int(currentNode[3])
					currentNode = self.decisionTree[curN + nextNode]
					curN = curN+nextNode

				#print "current Node", currentNode
				feature = int(currentNode[0])
				splitVal = currentNode[1]

			#print "classified done"
		arrayY = np.asarray(dataY)
		return arrayY

	def build_tree(self, dataX, dataY):
		
		#print "Data X = ", dataX

		#Check for stopping criteria first
		#If amount of data is <= maximum leaf size you are at a leaf node
		if dataX.shape[0] <= self.leaf_size:
			mode = stats.mode(dataY)
			leaf = np.array([-1, mode[0][0], np.nan, np.nan])
			return leaf

		#If all data is the same you are at a leaf node
		if np.unique(dataY).shape[0] == 1:
			leaf = np.array([-1, dataY[0], np.nan, np.nan])
			return leaf

		#Not at leaf node, need to spit
		feature = np.random.randint(0, dataX.shape[1])
		r1 = np.random.randint(0, dataX.shape[0])
		r2 = np.random.randint(0, dataX.shape[0])
		splitVal = (dataX[r1, feature] + dataX[r2, feature])/2.0
		split = dataX[:, feature] <= splitVal

		if np.alltrue(split) or np.alltrue(~split):
			mode = stats.mode(dataY)
			leaf = np.array([-1, mode[0][0], np.nan, np.nan])
			return leaf

		leftTree = self.build_tree(dataX[split, :], dataY[split])
		rightTree = self.build_tree(dataX[~split, :], dataY[~split])

		if leftTree.ndim == 1:
			root = np.array([feature, splitVal, 1, 2])
		else:
			root = np.array([feature, splitVal, 1, leftTree.shape[0]+1])


		tree = np.vstack((root, leftTree, rightTree))
		return tree

import pandas as pd 
import numpy as np
import datetime as dt
import Equity as eq
import portfolio as pf
import BagLearner as bl 
import RTLearner as rt
from Calculations import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy import optimize	

def addEvidence(prices, evidence, symbol):
	pass


def testPolicy():
	pass



def goldenCrossStrategy(syms=['GOOG','AAPL','GLD','XOM']):
	learner =  bl.BagLearner(learner = rt.RTLearner, kwargs={"leaf_size": 5})
	portfolio = pf.Portfolio(syms)
	prices = portfolio.get_data(size='full')
	train_prices = prices.loc['2015-01-09':'2018-01-07', :]

	norm_pricesAll = normalizeData(prices)
	norm_pricesTrain = normalizeData(train_prices)
	short_term = calculate_sma(norm_pricesAll, window=50)
	long_term = calculate_sma(norm_pricesAll, window=200)
	
	short_termTrain = short_term.loc['2015-01-09':'2018-01-07', :]
	long_termTrain = long_term.loc['2015-01-09':'2018-01-07', :]

	for stock in portfolio.port:
		print(stock.symbol)
		norm_prices = norm_pricesTrain[stock.symbol]
		df = pd.DataFrame(index=norm_pricesTrain.index)
		df['prices'] = norm_pricesTrain[stock.symbol]
		df['short term sma'] = short_termTrain[stock.symbol]
		df['long term sma'] = long_termTrain[stock.symbol]
		#df['volume'] = portfolio.get_volume(stock.symbol)
		df = df[:-2]

		x_train = df.values
		y_train = []

		
		for i in range(0, norm_prices.shape[0]-2):
			if (norm_prices.iloc[i+2] - norm_prices.iloc[i])/norm_prices.iloc[i] > 0.01:
				y_train.append(1)
			elif (norm_prices.iloc[i+2] - norm_prices.iloc[i])/norm_prices.iloc[i] < -0.01:
				y_train.append(-1)
			else:
				y_train.append(0)

		y_train = np.array(y_train)
		learner.addEvidence(x_train, y_train)

		test_prices = prices.loc['2018-06-01':'2019-04-25', :]
		norm_pricesTest = normalizeData(test_prices)
		short_termTest = short_term.loc['2018-06-01':'2019-04-25', :]
		long_termTest = long_term.loc['2018-06-01':'2019-04-25', :]
		df2 = pd.DataFrame(index=norm_pricesTest.index)
		df2['prices'] = norm_pricesTest[stock.symbol]
		df2['short term sma'] = short_termTest[stock.symbol]
		df2['long term sma'] = long_termTest[stock.symbol]
		#df['volume'] = portfolio.get_volume(stock.symbol)

		x_test = df2.values
		y_test = learner.query(x_test)

		print(x_test)
		print(y_test)



if __name__ == "__main__":
	goldenCrossStrategy()
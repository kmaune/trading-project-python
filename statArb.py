import pandas as pd 
import numpy as np
import datetime as dt
import Equity as eq
import portfolio as pf
from Calculations import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy import optimize	

##difference between R_{i,t} and R_{j,t} ???

def statArb():
	portfolio = pf.Portfolio(['GOOG','AAPL','GLD','XOM'])
	prices = portfolio.get_data(size='full')

	##Setting initial risk free rate to 3% for testing
	risk_free = 0.03

	dailyReturns = get_daily_returns(prices)
	adjustedReturns = dailyReturns - risk_free

	##Treating R_{i,t} and R{j,t} the same for now for Γ matrix from paper
	denom = adjustedReturns*adjustedReturns

	## γ matrix from paper
	gamma = adjustedReturns*risk_free

	plt.close()
	plt.figure()
	plt.title('Arbitrage Frontier')
	plt.xlabel('alpha_0 value')
	plt.ylabel('Phi Value (Std. Deviation)')

	##Temporary Optimal Weights and initial variance
	optimalWeights = -gamma/denom;
	variance = 0.0
	all_variances = []

	## mean return from 0% - 200% w/ 5% increments
	for alpha_0 in np.arange(0, 2.0, 0.05):
		Beta = ( (alpha_0*adjustedReturns) - gamma)/denom

		temp = Beta*adjustedReturns
		temp = temp + risk_free - alpha_0;
		temp = temp.sum(axis=1)
		temp=temp**2

		variance = temp.sum(axis=0)/temp.shape[0]
		std_dev = variance**(1/2)

		plt.plot(alpha_0, std_dev, '-ro')

	plt.show()




if __name__ == "__main__":
	statArb()
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
	riskFree = 0.03
	daily_riskFree = math.log(1+riskFree)/365

	dailyReturns = get_daily_returns(prices)
	adjustedReturns = dailyReturns - daily_riskFree

	##Treating R_{i,t} and R{j,t} the same for now for Γ matrix from paper
	denom = adjustedReturns*adjustedReturns

	## γ matrix from paper
	gamma = adjustedReturns*daily_riskFree

	plt.close()
	plt.figure(1)
	plt.title('Risk vs Return w/ optimal weights')
	plt.xlabel('alpha_0')
	plt.ylabel('Std. Deviation')
	plt.figure(2)
	plt.title('Return vs Log Likelihood')
	plt.xlabel('alpha_0')
	plt.ylabel(' Negative Log Likelihood')


	##Temporary Optimal Weights and initial variance
	optimalWeights = -gamma/denom;
	best_ll = -1.0

	ll_best_params = {}

	#print(adjustedReturns)
	#print(gamma)
	#print(denom)

	## mean return from 0% - 200% w/ 5% increments
	for alpha_0 in np.arange(0, 2.0, 0.05):
		Beta = ( (alpha_0*adjustedReturns) - gamma)/denom
		temp = Beta*adjustedReturns
		temp = temp + daily_riskFree - alpha_0;
		temp = temp.sum(axis=1)
		temp=temp**2

		#print(Beta)

		variance = temp.sum(axis=0)/temp.shape[0]
		std_dev = variance**(1/2)

		plt.figure(1)
		plt.plot(alpha_0, std_dev, '-ro')

		log_likelihood = get_log_likelihood(alpha_0, variance, Beta, dailyReturns,daily_riskFree)
		plt.figure(2)
		plt.plot(alpha_0, log_likelihood, '-bo')

		if best_ll < log_likelihood:
			ll_best_params = {}
			ll_best_params['ll'] = log_likelihood
			ll_best_params['alpha'] = alpha_0
			ll_best_params['variance'] = variance



	plt.show()



if __name__ == "__main__":
	statArb()
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

def statArb():
	portfolio = pf.Portfolio(['GOOG','AAPL','GLD','XOM'])
	prices = portfolio.get_data(size='full')

	##Setting initial risk free rate to 3% for testing
	riskFree = 0.03
	daily_riskFree = math.log(1+riskFree)/365

	dailyReturns = get_daily_returns(prices)
	adjustedReturns = dailyReturns - daily_riskFree

	#averageReturns = adjustedReturns.mean()

	beta_df = pd.DataFrame(index=adjustedReturns.index, columns=adjustedReturns.columns)

	for i in range(320, len(adjustedReturns)):
		subset_adjustedReturns = adjustedReturns.iloc[i-319:i, :]
		averageReturns = subset_adjustedReturns.mean()

		##Treating R_{i,t} and R{j,t} the same for now for Γ matrix from paper
		helper = adjustedReturns*adjustedReturns
		averageHelper = helper.mean()
		averageHelper_transposed = averageHelper.values

		Gamma = pd.DataFrame(1, index=averageHelper.index, columns=adjustedReturns.columns)
		Gamma = Gamma*averageHelper
		Gamma_transpose = Gamma.transpose()
		Gamma = Gamma*Gamma_transpose
		Gamma_inv = pd.DataFrame(np.linalg.pinv(Gamma.values), Gamma.columns, Gamma.index)


		## γ matrix from paper
		gamma = adjustedReturns*daily_riskFree
		average_gamma = gamma.mean()

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
		optimalWeights = -average_gamma/Gamma;
		best_ll = -1.0

		ll_best_params = {}

		alpha_0 = 0.005
		Beta = ((alpha_0*averageReturns) - average_gamma)
		Beta = Beta.dot(Gamma_inv)
		beta_df.iloc[i] = Beta

		temp = Beta.values*adjustedReturns
		temp = temp + daily_riskFree - alpha_0;
		temp = temp.sum(axis=1)
		temp=temp**2

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


	beta_df.dropna(axis=0, inplace=True)
	#plt.show()



if __name__ == "__main__":
	statArb()
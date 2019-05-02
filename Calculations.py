import pandas as pd 
import numpy as np
import math


def normalizeData(prices):
	return prices/prices.iloc[0, :]

def get_sma(prices, window=15):
	return prices.rolling(window).mean()


def get_daily_returns(prices):
	return prices / prices.shift(1) - 1

def get_log_likelihood(alpha, variance, weights, dailyReturns, daily_riskFree):
	#print(weights)
	adjustedReturns = dailyReturns - daily_riskFree
	days = dailyReturns.shape[0]
	std_dev = variance**(1/2)

	temp = weights*adjustedReturns
	temp = temp + daily_riskFree
	totalDailyReturns = temp.sum(axis=1)
	totalDailyReturns = totalDailyReturns - alpha
	totalDailyReturns = totalDailyReturns**2
	#print(totalDailyReturns)

	totalReturns = totalDailyReturns.sum(axis=0)
	#print(totalReturns/(2*days*variance))

	return math.log(std_dev) + (0.5*math.log(2*math.pi)) + (totalReturns/(2*days*variance))



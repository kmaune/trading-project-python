import pandas as pd 
import numpy as np 


def normalizeData(prices):
	return prices/prices.iloc[0, :]

"""
	Needed since alpha vantage API does not have adjusted close
	option for calculating sma
"""
def calculate_sma(prices, window=15):
	return prices.rolling(window).mean()


def get_daily_returns(prices):
	return prices / prices.shift(1) - 1




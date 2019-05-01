import pandas as pd 
import numpy as np
import datetime as dt
import Equity as eq
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy import optimize	


class Portfolio(object):

	def __init__(self, syms=['GOOG','AAPL','GLD','XOM']):
		self.symbols = syms
		self.port = []
		for symbol in syms:
			asset = eq.Equity(symbol=symbol)
			self.port.append(asset)
		self.weights = np.ones((1, len(syms)))/len(syms)
	
	def get_data(self, type='daily', size='compact'):
		if type == 'daily':
			data = self.port[0].get_daily(size)
			df = pd.DataFrame(index=data.index)
			df[self.port[0].symbol] = data['adjusted close']

			for i in range(1, len(self.port)):
				data = self.port[i].get_daily(size)
				df[self.port[i].symbol] = data['adjusted close']
			#print(df)
			return df
			
		elif type =='intra_day':
			data = self.port[0].get_intraday(size)
			df = pd.DataFrame(index=data.index)
			df[self.port[0].symbol] = data['close']

			for i in range(1, len(self.port)):
				data = self.port[i].get_intraday(size)
				df[self.port[i].symbol] = data['close']
			return df

		elif type == 'weekly':
			data = self.port[0].get_weekly(size)
			df = pd.DataFrame(index=data.index)
			df[self.port[0].symbol] = data['adjusted close']

			for i in range(1, len(self.port)):
				data = self.port[i].get_weekly(size)
				df[self.port[i].symbol] = data['adjusted close']
			return df
			

		elif type == 'monthly':
			data = self.port[0].get_monthly(size)
			df = pd.DataFrame(index=data.index)
			df[self.port[0].symbol] = data['adjusted close']

			for i in range(1, len(self.port)):
				data = self.port[i].get_monthly(size)
				df[self.port[i].symbol] = data['adjusted close']
			return df

		else:
			pass
			##Raise error
		
	def get_volume(symbol):
		asset = eq.Equity(symbol=symbol)
		data = asset.get_daily()
		return data['volume']




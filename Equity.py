import pandas as pd
import numpy as np
import datetime as dt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

class Equity(object):

	def __init__(self, symbol='AAPL', apiKey='GVGPTAMVFRX2Y8OY'):
		self.symbol = symbol
		self.apiKey = apiKey
		self.ts = TimeSeries(key=self.apiKey, output_format='pandas', indexing_type='date')
		self.ti = TechIndicators(key=self.apiKey, output_format='pandas')

	def get_intraday(self, time_interval='15min', size='compact'):
		data, meta_data = self.ts.get_intraday(self.symbol, time_interval, size)
		data.columns = ['open', 'high', 'low', 'close', 'volume']
		return data

	"""
	def get_daily(self, size='compact'):
		data, meta_data = self.ts.get_daily(self.symbol, size)
		data.columns = ['open', 'high', 'low', 'close', 'volume']
		return data
	"""
	def get_daily(self, size='compact'):
		data, meta_data = self.ts.get_daily_adjusted(self.symbol, size)
		data.columns = ['open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount', 'split coefficient']
		return data

	"""
	def get_weekly(self, sym):
		data, meta_data = self.ts.get_weekly(self.symbol)
		data.columns = ['open', 'high', 'low', 'close', 'volume']
		return data
	"""

	def get_weekly(self):
		data, meta_data = self.ts.get_weekly_adjusted(self.symbol)
		data.columns = ['open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount']
		return data

	"""
	def get_monthly(self, sym):
		data, meta_data = self.ts.get_monthly(self.symbol)
		data.columns = ['open', 'high', 'low', 'close', 'volume']
		return data
	"""

	def get_monthly(self):
		self.data, meta_data = self.ts.get_monthly_adjusted(self.symbol)
		self.data.columns = ['open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount']
		return self.data


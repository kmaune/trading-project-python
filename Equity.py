import pandas as pd
import numpy as np
import datetime as dt
from alpha_vantage.timeseries import TimeSeries

class Equity(object):

	def __init__(self, symbol='AAPL', apiKey='GVGPTAMVFRX2Y8OY'):
		self.symbol = symbol
		self.apiKey = apiKey
		self.ts = TimeSeries(key=self.apiKey, output_format='pandas', indexing_type='date')

	def get_intraday(self, time_interval='15min', size='compact'):
		data, meta_data = self.ts.get_intraday(self.symbol, time_interval, size)

	def get_daily(self, size='compact'):
		data, meta_data = self.ts.get_daily(self.symbol, size)
		data.columns = ['open', 'high', 'low', 'close', 'volume']
		return data

	def get_dailyAdjusted(self, sym, size='compact'):
		data, meta_data = self.ts.get_daily_adjusted(sym, size)
		data.columns = ['open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount', 'split coefficient']
		return data

	def get_weekly(self, sym):
		data, meta_data = self.ts.get_weekly(self.symbol)
		data.columns = ['open', 'high', 'low', 'close', 'volume']
		return data

	def get_weeklyAdjusted(self, sym):
		data, meta_data = self.ts.get_weekly_adjusted(self.symbol)
		data.columns = ['open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount']
		return data

	def get_monthly(self, sym):
		data, meta_data = self.ts.get_monthly(self.symbol)
		data.columns = ['open', 'high', 'low', 'close', 'volume']
		return data

	def get_monthlyAdjusted(self, sym):
		data, meta_data = self.ts.get_monthly_adjusted(self.symbol)
		data.columns = ['open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend amount']
		return data

	def normalizeDaily(self, data, adjusted=False):
		if adjusted==False:
			volume = data['volume']
			data = data/data.iloc[0, :]
			data['volume'] = volume
		else:
			volume = data['volume']
			div = data['dividend amount']
			split = data['split coefficient']
			data = data/data.iloc[0, :]
			data['volume']= volume
			data['dividend amount'] = div
			data['split coefficient'] = split
		return data


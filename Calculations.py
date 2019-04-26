import pandas as pd 
import numpy as np 


def normalizeData(prices):
	return prices/prices.iloc[0, :]



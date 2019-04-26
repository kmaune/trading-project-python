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

def run_test():
	#asset = eq.Equity(symbol='AAPL')
	#data = asset.get_daily()
	#print(data)

	port = pf.Portfolio()
	prices = port.get_data()
	print(prices)
	normalized_prices = normalizeData(prices)
	print(normalized_prices)


	bounds = [(0.0, 1.0)] * len(port.symbols)
	constraints = ({ 'type': 'eq', 'fun': lambda x: np.sum(x) - 1 })
	weights = np.ones((1, len(port.symbols)))/len(port.symbols)	
	min_optimizer = optimize.minimize(port.optimizeSharpe, weights, args=(prices), method='SLSQP', bounds=bounds, constraints=constraints)
	optimal_weights = np.asarray(min_optimizer.x)
	original = [1/len(port.symbols) for i in range(0, len(port.symbols))]

	print(optimal_weights.shape)

	plt.close()
	plt.figure()
	#Plot original weights	
	plt.plot(original, color='blue', marker='o', linestyle='solid')
	#plot optimal calculated weights
	plt.plot(optimal_weights, color='green', marker='o', linestyle='solid')
	plt.title("Original Weights vs Optimal Weights")
	xi = [i for i in range(0, len(port.symbols))]
	plt.xticks(xi, port.symbols)
	plt.show()

	

if __name__ == "__main__":
	run_test()
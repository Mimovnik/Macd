import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('wig20_2019-2024.csv')

ema12 = df['Zamkniecie'].rolling(window=12, min_periods=1).mean()
ema26 = df['Zamkniecie'].rolling(window=26, min_periods=1).mean()

macd = ema12 - ema26

signal = macd.rolling(window=9, min_periods=1).mean()

buy_points = np.where((macd > signal) & (
    macd.shift(1) < signal.shift(1)), macd, np.nan)

sell_points = np.where((macd < signal) & (
    macd.shift(1) > signal.shift(1)), macd, np.nan)


# Plotting
plt.figure(figsize=(18, 8))

plt.subplot(2, 1, 1)
plt.plot(df['Zamkniecie'], label='Close Price', color='blue')
plt.title('Close Price')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(macd, label='MACD', color='blue')
plt.plot(signal, label='SIGNAL', color='red')
plt.scatter(df.index, buy_points, color='green',
            marker='^', label='Buy Signal')
plt.scatter(df.index, sell_points, color='orange',
            marker='v', label='Sell Signal')
plt.title('MACD, SIGNAL and buy/sell signals')
plt.legend()

plt.show()

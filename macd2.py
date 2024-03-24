import pandas as pd
import matplotlib.pyplot as plt


def ema(data, n):
    if n <= 0 or n > len(data):
        raise ValueError("Invalid number of periods.")
    alpha = 2 / (n + 1)
    ema_values = [data[0]]
    for i in range(1, len(data)):
        ema = alpha * data[i] + (1 - alpha) * ema_values[-1]
        ema_values.append(ema)

    return ema_values


df = pd.read_csv('wig20_2019-2024.csv')
data = df['Zamkniecie'].tolist()
print("data len " + str(len(data)))

ema12 = ema(data, 12)
print("ema12 len " + str(len(ema12)))
ema26 = ema(data, 26)
print("ema26 len " + str(len(ema26)))

macd = []
for i in range(len(ema12)):
    macd.append(ema12[i] - ema26[i])

signal = ema(macd, 9)

buy_points = [None]
sell_points = [None]
for i in range(1, len(macd)):
    if macd[i] > signal[i] and macd[i - 1] < signal[i - 1]:
        buy_points.append(macd[i])
    else:
        buy_points.append(None)

    if macd[i] < signal[i] and macd[i - 1] > signal[i - 1]:
        sell_points.append(macd[i])
    else:
        sell_points.append(None)

print("buy_points len " + str(len(buy_points)))
print("sell_points len " + str(len(sell_points)))

indexes = list(range(len(data)))
# Plotting
plt.figure(figsize=(18, 8))

plt.subplot(2, 1, 1)
plt.plot(df['Data'], data, label='Close Price', color='blue')
plt.xticks(df['Data'][::100])
plt.title('Close Price')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(macd, label='MACD', color='blue')
plt.plot(signal, label='SIGNAL', color='red')
plt.scatter(indexes, buy_points, color='green',
            marker='^', label='Buy Signal')
plt.scatter(indexes, sell_points, color='orange',
            marker='v', label='Sell Signal')
plt.title('MACD, SIGNAL and buy/sell signals')
plt.legend()

plt.show()

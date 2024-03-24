import pandas as pd
import matplotlib.pyplot as plt


def ema(data, n):
    if n <= 0 or n > len(data):
        raise ValueError("Invalid number of periods.")
    alpha = 2 / (n + 1)
    ema_values = [data[0]]
    for i in range(1, n):
        ema = alpha * data[i] + (1 - alpha) * ema_values[-1]
        ema_values.append(ema)

    return ema_values[-1]


df = pd.read_csv('wig20_2019-2024.csv')
data = df['Zamkniecie'].tolist()
data = data[:1035]
print("data len " + str(len(data)))

macd = []
signal = []
for i in range(26, len(data)):
    ema12 = ema(data[i - 12:i], 12)
    ema26 = ema(data[i - 26:i], 26)
    macd.append(ema12 - ema26)

data = data[len(data)-1000:]
print("data len " + str(len(data)))

print("macd len " + str(len(macd)))

for i in range(9, len(macd)):
    signal.append(ema(macd[i - 9:i], 9))

macd = macd[len(macd)-1000:]
print("macd len " + str(len(macd)))
print("signal len " + str(len(signal)))

buy_points = [None]
sell_points = [None]
for i in range(1, len(macd)):
    if macd[i] > signal[i] and macd[i - 1] < signal[i - 1]:
        buy_points.append(signal[i])
    else:
        buy_points.append(None)

    if macd[i] < signal[i] and macd[i - 1] > signal[i - 1]:
        sell_points.append(signal[i])
    else:
        sell_points.append(None)

print("buy_points len " + str(len(buy_points)))
print("sell_points len " + str(len(sell_points)))

# Plotting

indexes = list(range(len(data)))
dates = df['Data'].tolist()[len(df['Data']) - 1000:]
plt.figure(figsize=(18, 8))

plt.subplot(2, 1, 1)
plt.plot(dates, data,
         label='Close Price', color='blue')
plt.xticks(dates[::100])
plt.title('WIG20 Close Price 2019-2024')
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

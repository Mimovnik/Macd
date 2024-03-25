import pandas as pd
import matplotlib.pyplot as plt


def ema(data, day_zero: int, n: int) -> float:
    if n <= 0 or n > len(data):
        raise ValueError("Invalid number of periods.")

    alpha = 2 / (n + 1)
    alpha_complement = 1 - alpha
    nominator, denominator = 0, 0
    factor = 1
    for i in range(n):
        nominator += data[day_zero - i] * factor
        denominator += factor
        factor *= alpha_complement

    return float(nominator / denominator)


# Load data
df = pd.read_csv("dane.csv")
dates = df['Data'].tolist()[len(df['Data']) - 1000:]

data = df['Zamkniecie'].tolist()
data = data[:1035]
print("data len " + str(len(data)))


# Calculate MACD and SIGNAL
macd = []
signal = []
for i in range(26, len(data)):
    ema12 = ema(data, i, 12)
    ema26 = ema(data, i, 26)
    macd.append(ema12 - ema26)

print("macd len " + str(len(macd)))

for i in range(9, len(macd)):
    signal.append(ema(macd, i, 9))

print("trim to 1000 elements")

data = data[len(data)-1000:]
print("data len " + str(len(data)))
macd = macd[len(macd)-1000:]
print("macd len " + str(len(macd)))
print("signal len " + str(len(signal)))

# Find buy and sell points
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

# Plot

indices = list(range(len(data)))
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(dates, data,
         label='Close Price', color='blue')
plt.xticks(dates[::100])
plt.title('WIG20 Close Price 2019-2024')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(macd, label='MACD', color='blue')
plt.plot(signal, label='SIGNAL', color='red')
plt.scatter(indices, buy_points, color='green',
            marker='^', label='Buy Signal')
plt.scatter(indices, sell_points, color='orange',
            marker='v', label='Sell Signal')
plt.title('MACD, SIGNAL and buy/sell signals')
plt.legend()

plt.show()

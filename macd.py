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
data2 = range(1, 20)
df2 = pd.DataFrame(data2)

ema12 = df2.rolling(window=12, min_periods=1).mean()

myema12 = ema(data2, 12)

for i in range(0, len(myema12)):
    print(str(i) + ". " + "e = " +
          str(ema12[0][i]) + "     mye  = " + str(myema12[i]))

print("ema12 size = " + str(len(ema12[0])))
print("myema12 size = " + str(len(myema12)))
exit(0)

macd = ema12 - ema26

signal = macd.rolling(window=9, min_periods=1).mean()

# buy_points = np.where((macd > signal) & (
#     macd.shift(1) < signal.shift(1)), macd, np.nan)
#
# sell_points = np.where((macd < signal) & (
#     macd.shift(1) > signal.shift(1)), macd, np.nan)


# Plotting
plt.figure(figsize=(18, 8))

plt.subplot(2, 1, 1)
plt.plot(df['Zamkniecie'], label='Close Price', color='blue')
plt.title('Close Price')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(macd, label='MACD', color='blue')
plt.plot(signal, label='SIGNAL', color='red')
# plt.scatter(df.index, buy_points, color='green',
#             marker='^', label='Buy Signal')
# plt.scatter(df.index, sell_points, color='orange',
#             marker='v', label='Sell Signal')
plt.title('MACD, SIGNAL and buy/sell signals')
plt.legend()

plt.show()

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


def calc_macd_signal(data, short_ema_period, long_ema_period, signal_period):
    macd = []
    for i in range(long_ema_period, len(data)):
        short_ema = ema(data, i, short_ema_period)
        long_ema = ema(data, i, long_ema_period)
        macd.append(short_ema - long_ema)

    print("macd len " + str(len(macd)))

    signal = []
    for i in range(signal_period, len(macd)):
        signal.append(ema(macd, i, signal_period))

    print("trim to " + str(sample_length) + " elements")

    data = data[len(data) - sample_length:]
    print("data len " + str(len(data)))
    macd = macd[len(macd) - sample_length:]
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
    return macd, signal, buy_points, sell_points


def plot_macd(data, macd, signal, buy_points, sell_points):
    indices = list(range(len(data)))
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(indices, data, label='Close Price', color='blue', linewidth=0.5)
    plt.title("Financial instrument quotations")
    plt.ylabel("Price")
    plt.xlabel("Date")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(macd, label='MACD', color='blue', linewidth=0.5)
    plt.plot(signal, label='SIGNAL', color='red', linewidth=0.5)
    plt.scatter(indices, buy_points, color='green',
                marker='^', label='Buy Signal')
    plt.scatter(indices, sell_points, color='orange',
                marker='v', label='Sell Signal')
    plt.title('MACD, SIGNAL and buy/sell signals')
    plt.ylabel('Value')
    plt.xlabel('Day')
    plt.legend()

    plt.show()


def run_macd(data, sample_length,
             short_ema_period, long_ema_period, signal_period):
    data = data[:sample_length + long_ema_period + signal_period]
    print("data len " + str(len(data)))

    macd, signal, buy_points, sell_points = calc_macd_signal(
        data, short_ema_period, long_ema_period, signal_period)

    data = data[:sample_length]
    plot_macd(data, macd, signal, buy_points, sell_points)


sample_length = 1000
short_ema_period = 12
long_ema_period = 26
signal_period = 9

df = pd.read_csv("wig20.csv")
data = df['Zamkniecie'].tolist()
run_macd(data, sample_length, short_ema_period, long_ema_period, signal_period)

df = pd.read_csv("sax.csv")
data = df['Zamkniecie'].tolist()
run_macd(data, sample_length, short_ema_period, long_ema_period, signal_period)

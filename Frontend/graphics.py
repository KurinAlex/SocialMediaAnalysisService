import numpy as np
import matplotlib as mpl
import matplotlib.dates as mdates
from matplotlib import pyplot as plt, gridspec

mpl.use("TkAgg")

def draw_graphs(keyword, data):
    fig = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1])
    ax1 = plt.subplot(gs[:, 0])
    ax2 = plt.subplot(gs[0, 1])
    ax3 = plt.subplot(gs[1, 1])
    draw_plot(keyword, data, ax=ax1)
    draw_bar_chart(keyword, data, ax=ax2)
    draw_circle_diagram(keyword, data, ax=ax3)
    plt.tight_layout()
    plt.show()

def draw_circle_diagram(keyword, data, ax=None):
    total_count = data["total"]["count"]
    positive_data = data["total"]["positive"]
    negative_data = data["total"]["negative"]
    neutral_data = data["total"]["neutral"]

    sizes = [positive_data, negative_data, neutral_data]
    labels = ['Positive', 'Negative', 'Neutral']
    exp = (0.1, 0.1, 0.3)
    labels_with_count = [f"{label}: {size}" for label, size in zip(labels, sizes)]
    colors = ['#00FF00', '#FF4500', '#00FFFF']

    if ax is None:
        plt.pie(sizes, labels=labels_with_count, colors=colors, autopct='%1.1f%%', explode=exp)
        plt.title("Total count of \'" + keyword + "\' phrase during last week is " + str(total_count))
        plt.show()
    else:
        ax.pie(sizes, labels=labels_with_count, colors=colors, autopct='%1.1f%%', explode=exp)
        ax.set_title("Total count of \'" + keyword + "\' phrase during last week is " + str(total_count))


def draw_bar_chart(keyword, data, ax=None):
    nouns_data = data["top20_nouns"]["nouns"]
    count_data = data["top20_nouns"]["count"]

    sorted_indices = np.argsort(count_data)[::-1]
    sorted_nouns = [nouns_data[i] for i in sorted_indices]
    sorted_counts = [count_data[i] for i in sorted_indices]

    if ax is None:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(sorted_nouns, sorted_counts, color='skyblue')
        plt.xticks(rotation=45, ha='right', fontsize=10)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), va='bottom', fontsize=9)

        plt.title('Top 20 Nouns of \'' + keyword + "\'")
        plt.xlabel('Nouns')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()
    else:
        ax.bar(sorted_nouns, sorted_counts, color='skyblue')
        ax.set_xticks(range(len(sorted_nouns)))
        ax.set_xticklabels(sorted_nouns, rotation=45, ha='right', fontsize=10)
        ax.set_title('Top 20 Nouns of \'' + keyword + "\'")
        ax.set_xlabel('Nouns')
        ax.set_ylabel('Frequency')

def draw_plot(keyword, data,ax):
    dates_data = data["daily"]["dates"]
    total_count_data = data["daily"]["count"]
    positive_data = data["daily"]["positive"]
    negative_data = data["daily"]["negative"]
    neutral_data = data["daily"]["neutral"]

    ax.plot(dates_data, total_count_data, label='Total Count', color='black', linestyle='-')
    ax.plot(dates_data, positive_data, label='Positive', color='#00FF00', linestyle='--')
    ax.plot(dates_data, negative_data, label='Negative', color='#FF4500', linestyle='-.')
    ax.plot(dates_data, neutral_data, label='Neutral', color='#00FFFF', linestyle=':')

    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Publications')
    ax.set_title("Publications per Day for \"" + keyword + "\" with Sentiment Breakdown")
    ax.grid(True)
    ax.legend()
    plt.xticks(rotation=45)  # Поворот підписів осі x
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Встановлення формату дати

    plt.tight_layout()
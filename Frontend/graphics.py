from matplotlib import gridspec, use
from matplotlib.dates import DateFormatter
from matplotlib.pyplot import Axes, get_current_fig_manager, figure

use("TkAgg")


def draw_graphs(keyword, data):
    fig = figure(figsize=(10, 14))

    gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1], figure=fig)
    ax1 = fig.add_subplot(gs[:, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 1])

    draw_plot(data, ax=ax1)
    draw_pir_chart(data, ax=ax2)
    draw_bar_chart(keyword, data, ax=ax3)

    fig_manager = get_current_fig_manager()
    fig_manager.set_window_title('NLP analysis')

    fig.subplots_adjust(wspace=0.4, hspace=0.6)
    fig.tight_layout()
    fig.show()


def draw_pir_chart(data: dict, ax: Axes) -> None:
    total_count = data["total"]["count"]
    positive_data = data["total"]["positive"]
    negative_data = data["total"]["negative"]
    neutral_data = data["total"]["neutral"]

    exp = (0.1, 0.1, 0.3)
    sizes = [positive_data, negative_data, neutral_data]
    labels = ['Positive', 'Negative', 'Neutral']
    labels_with_count = [f"{label}: {size}" for label, size in zip(labels, sizes)]
    colors = ['#00FF00', '#FF4500', '#00FFFF']

    ax.pie(sizes, labels=labels_with_count, colors=colors, autopct='%1.1f%%', explode=exp)
    ax.set_title(f"Total sentiment distribution of {total_count} articles")


def draw_bar_chart(keyword: str, data: dict, ax: Axes) -> None:
    nouns_data = data["top20_nouns"]["nouns"]
    count_data = data["top20_nouns"]["count"]

    ax.bar(nouns_data, count_data, color='skyblue')
    ax.set_xticks(range(len(nouns_data)))
    ax.set_xticklabels(nouns_data, rotation=35, ha='right', fontsize=8)
    ax.set_title(f'Top 20 Nouns, associated with {keyword} by frequency of mentioning')
    ax.set_xlabel('Nouns')
    ax.set_ylabel('Frequency')


def draw_plot(data: dict, ax: Axes) -> None:
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
    ax.set_title(" Sentiment Breakdown of Daily Publications")
    ax.grid(True)
    ax.legend()
    ax.set_xticklabels(dates_data, rotation=25, ha='right', fontsize=10)
    ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y'))

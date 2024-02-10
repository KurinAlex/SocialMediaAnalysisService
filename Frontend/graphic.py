from datetime import datetime, timedelta

import numpy as np
import matplotlib as mpl
import Backend.main as backend
from matplotlib import pyplot as plt

mpl.use("TkAgg")

def draw_circle_diagram(keyword , data):
    data = backend.get_default_analysis(keyword, (datetime.now() - timedelta(days=7)).date())

    total_count = data["total"]["count"]
    positive_data = data["total"]["positive"]
    negative_data = data["total"]["negative"]
    neutral_data = data["total"]["neutral"]

    sizes = [positive_data, negative_data, neutral_data]
    labels = ['Positive', 'Negative', 'Neutral']
    exp = (0.1, 0.1, 0.3)
    labels_with_count = [f"{label}: {size}" for label, size in zip(labels, sizes)]
    colors = ['#00FF00', '#FF4500', '#00FFFF']

    plt.pie(sizes, labels=labels_with_count, colors=colors, autopct='%1.1f%%', explode=exp)
    plt.title("Total count of \"" + keyword + "\" phrase during last week is " + str(total_count))
    plt.show()

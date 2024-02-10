import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

mpl.use("TkAgg")

def draw_circle_diagram(data):
    positive_data = data["total"]["positive"]
    negative_data = data["total"]["negative"]
    neutral_data = data["total"]["neutral"]
    plt.pie([positive_data, negative_data, neutral_data], labels=['Positive', 'Negative', 'Neutral'])
    plt.show()
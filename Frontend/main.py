import tkinter as tk
from tkcalendar import Calendar

from Frontend.api_keys import news_api_key, event_registry_api_key
import Frontend.graphics as graphic

from Backend.main import get_analysis
from Backend.data_providers import NewsApiDataProvider, EventRegistryDataProvider

win = tk.Tk()

social_media_analysis_service_label = tk.Label(
    win,
    text="Social media analysis service",
    background="#E0FFFF",
    padx=20,
    pady=40,
    font=('Georgia', 20, 'bold', 'italic')
)

choose_your_date_here_label = tk.Label(
    win,
    text="Choose date here:",
    background="#E0FFFF",
    padx=20,
    pady=15,
    font=('Georgia', 14)
)

entry_text = tk.StringVar()
entry_text.set("#socialmedia")

calendar = Calendar(win, selectmode='day', year=2024, month=2, day=10)


def analyze():
    keyword = entry_text.get()
    min_published_date = calendar.selection_get()
    providers = [NewsApiDataProvider(news_api_key), EventRegistryDataProvider(event_registry_api_key)]
    max_items_per_provider = 100

    data = get_analysis(keyword, min_published_date, providers, max_items_per_provider)
    graphic.draw_graphs(entry_text.get(), data)


get_keyword_entry = tk.Entry(win, width=20, font=('Arial', 16), textvariable=entry_text)
analise_button = tk.Button(win, width=10, text="Analise", padx=20, pady=10, command=analyze)

win.config(background="#E0FFFF")
win.title("Social media analysis service")
win.geometry("500x500")
win.resizable(False, False)
social_media_analysis_service_label.pack()
get_keyword_entry.pack()
choose_your_date_here_label.pack()
calendar.pack()
analise_button.pack(pady=25)

win.mainloop()

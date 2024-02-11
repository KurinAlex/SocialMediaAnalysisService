from tkinter import Tk, Label, Button, StringVar, Entry
from tkinter.messagebox import showerror

from tkcalendar import Calendar

from Backend.api_keys import news_api_key, event_registry_api_key
from Backend.data_providers import NewsApiDataProvider, EventRegistryDataProvider
from Backend.main import get_analysis
from Frontend.graphics import draw_graphs

# create window
win = Tk()

# set main label
social_media_analysis_service_label = Label(
    win,
    text="Social media analysis service",
    background="#E0FFFF",
    padx=20,
    pady=40,
    font=('Georgia', 20, 'bold', 'italic')
)

# set calendar label
choose_your_date_here_label = Label(
    win,
    text="Choose date here:",
    background="#E0FFFF",
    padx=20,
    pady=15,
    font=('Georgia', 14)
)

entry_text = StringVar(value="Ukraine")  # entry text for keyword input
calendar = Calendar(win, selectmode='day', year=2024, month=2, day=10)  # calendar for date choosing


def analyze():
    try:
        # set parameters
        keyword = entry_text.get()
        min_published_date = calendar.selection_get()
        providers = [NewsApiDataProvider(news_api_key), EventRegistryDataProvider(event_registry_api_key)]
        max_items_per_provider = 100

        # get analysis data
        data = get_analysis(keyword, min_published_date, providers, max_items_per_provider)

        # draw graphs
        draw_graphs(entry_text.get(), data)

    except Exception as ex:
        # show message box with error message in case of exception
        showerror(title='An error occurred!', message=str(ex))


# set text entry and button
get_keyword_entry = Entry(win, width=20, font=('Arial', 16), textvariable=entry_text)
analise_button = Button(win, width=10, text="Analyze", padx=20, pady=10, command=analyze)

# set window parameters
win.config(background="#E0FFFF")
win.title("Social media analysis service")
win.geometry("500x500")
win.resizable(False, False)

# pack components
social_media_analysis_service_label.pack()
get_keyword_entry.pack()
choose_your_date_here_label.pack()
calendar.pack()
analise_button.pack(pady=25)

# run main loop
win.mainloop()

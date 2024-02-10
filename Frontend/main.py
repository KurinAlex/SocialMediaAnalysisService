import tkinter as tk

from tkcalendar import Calendar

win = tk.Tk()

social_media_analysis_service_label = tk.Label(win, text="Social media analysis service",
                                               background="#E0FFFF",
                                               padx=20,
                                               pady=40,
                                               font=('Georgia', 20, 'bold', 'italic'))

get_keyword_entry = tk.Entry(win, width=20, font=('Arial', 16))

callendar = Calendar(win, selectmode='day', year=2024, month=2, day=10)

win.config(background="#E0FFFF")
win.title("Social media analysis service")
win.geometry("500x500")
win.resizable(False, False)
social_media_analysis_service_label.pack()
get_keyword_entry.pack()
callendar.pack_forget()
win.mainloop()

import tkinter
from tkinter.ttk import Label, Entry, Button, Scrollbar

from PIL import ImageTk, Image

root = tkinter.Tk()
root.geometry("720x400")
frame = tkinter.Frame(root)
frame.pack()

## url label
url_label = Label(frame, text="Video URL")
url_label.grid(row=0, column=0, padx=8, pady=8)

## URL entry
url_entry = Entry(frame, width=64)
url_entry.insert(0, '')
url_entry.grid(row=0, column=1, padx=8, pady=8)

## search button
search_button = Button(frame, text="Search", command=None)
search_button.grid(row=0, column=3, padx=8, pady=8)

root.title("Youtube Downloader")
root.mainloop()

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

root.title("Youtube Downloader")
root.mainloop()

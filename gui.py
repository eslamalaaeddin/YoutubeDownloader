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

## thumbnail
img = ImageTk.PhotoImage(Image.open("jerry.jpg").resize((196, 196)))
panel = Label(frame, image=img, anchor="w")
panel.grid(row=2, column=0, padx=8, pady=8)

## streams list box
streams_listbox = tkinter.Listbox(frame)

for i in range(100):
    streams_listbox.insert(str(i), ' ------------------- ' + str(i + 1))

streams_listbox.grid(row=2, column=1, padx=8, pady=8, sticky='EW')

# myscroll = Scrollbar(frame, orient='vertical')
# myscroll.grid(row=2, column=1, sticky='ns')
# myscroll.config(command = streams_listbox.yview)

root.title("Youtube Downloader")
root.mainloop()

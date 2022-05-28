import tkinter
from tkinter import CENTER, HORIZONTAL, END, DISABLED, NORMAL
from tkinter.ttk import Label, Entry, Button, Progressbar
import requests
from io import BytesIO
import pytube
from PIL import ImageTk, Image

import threading

# import commands
from pytube import YouTube


def open_popup(text):
    top = tkinter.Toplevel(root)
    width = 320
    height = 224
    top.geometry(str(width) + "x" + str(height))
    top.title("Info")
    Label(top, text=text, font=('Mistral 16 bold'), justify='center').place(relx=0.5, rely=0.5, anchor=CENTER)


def progress_Check(stream=None, chunk=None, remaining=0):
    # global file_size
    # percent = file_size - remaining + 1000000
    #
    # try:
    #     # updates the progress bar
    #     download_progress_bar.update()
    # except:
    #     # progress bar dont reach 100% so a little trick to make it 100
    #     download_progress_bar.update()
    # print('something')
    pass


def on_search_complete():
    # print('Searching completed')
    # response = requests.get(yt.thumbnail_url)
    # img = Image.open(BytesIO(response.content))
    # # img.show()
    # img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((196, 196)))
    # panel = Label(frame, image=img, anchor="w")
    # panel.grid(row=2, column=0, padx=8, pady=8)
    # switch()
    pass


def switch_search_button_state():
    print(search_button['state'])
    if search_button['state'] == 'normal':
        search_button['state'] = 'disabled'
        # print('a')
    else:
        search_button['state'] = 'normal'
        # print('b')


def show_all_streams(url):
    yt = None
    try:
        yt = YouTube(url=url, on_progress_callback=progress_Check(), on_complete_callback=on_search_complete())
        response = requests.get(yt.thumbnail_url)
        img = Image.open(BytesIO(response.content))
        # img.show()
        img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((196, 196)))

        panel.configure(image=img)
        panel.image = img


    except Exception as e:
        print(e)

    return yt, yt.streams.filter(progressive=True).otf(False), yt.streams.filter(
        type='audio') if yt is not None else None


def on_search_button_clicked():
    url = url_entry.get()

    streams_listbox.delete(0, END)
    global video_streams
    global audio_streams
    global yt
    # yt, streams = commands.search_with_url(url)
    yt, video_streams, audio_streams = show_all_streams(url)

    if audio_streams is not None:
        for i, s in enumerate(audio_streams):
            # print(s)
            media_label = s.title + ' - ' + str(s.abr) + ' - ' + str(round(s.filesize / 1000000, 2)) + 'MB'
            # print(s)
            streams_listbox.insert(i, media_label + '|' + str(s.itag))

    if video_streams is not None:
        for i, s in enumerate(video_streams):
            # print(s)
            if s.type == 'video':
                media_label = s.title + ' - ' + str(s.resolution) + ' - ' + str(s.fps) + 'fps' + ' - ' + str(
                    round(s.filesize / 1000000, 2)) + 'MB'
            else:
                media_label = s.title + ' - ' + str(s.abr) + ' - ' + str(round(s.filesize / 1000000, 2)) + 'MB'
            # print(s)
            streams_listbox.insert(i, media_label + '|' + str(s.itag))

    else:
        print('Error')

    switch_search_button_state()


def search_threaded():
    global search_thread
    switch_search_button_state()
    search_thread = threading.Thread(target=on_search_button_clicked, daemon=True)
    search_thread.start()


def download_threaded():
    global download_thread
    download_thread = threading.Thread(target=download_selected, daemon=True).start()


def cancel_download():
    download_thread = None


def download_selected():
    selected = streams_listbox.curselection()  # returns a tuple
    if not selected:
        info = "اختار حاجة أحملها لك الأول يا حلوف".split(' ')
        info.reverse()
        info = ' '.join(info)
        open_popup(info)

    for idx in selected:
        itag = streams_listbox.get(idx).rpartition('|')[-1]
        print('Downloading ', idx, itag)
        aud_streams = audio_streams.get_by_itag(itag)
        vid_streams = video_streams.get_by_itag(itag)

        if vid_streams is not None:
            print(vid_streams.filesize)
            vid_streams.download(
                output_path=output_path_entry.get(),
                filename_prefix=itag)
            print('Download Completed')

            # TODO PROGRESSING STUFF

        if aud_streams is not None:
            print(aud_streams.filesize)
            aud_streams.download(
                output_path=output_path_entry.get(),
                filename_prefix=itag)
            print('Download Completed')

            # TODO PROGRESSING STUFF


root = tkinter.Tk()
root.geometry("800x400")
frame = tkinter.Frame(root)
frame.pack()



# img = ImageTk.PhotoImage(Image.open("jerry.jpg").resize((196, 196)))

## url label
url_label = Label(frame, text="Video URL")
url_label.grid(row=0, column=0, padx=8, pady=4)

## URL entry
url_entry = Entry(frame, width=64)
url_entry.insert(0, 'https://www.youtube.com/watch?v=54_XRjHhZzI')
url_entry.grid(row=0, column=1, padx=8, pady=4)

## output path label
output_path_label = Label(frame, text="Download path")
output_path_label.grid(row=1, column=0, padx=8, pady=4)

## output entry
output_path_entry = Entry(frame, width=64)
output_path_entry.insert(0,
                         'C:\\Users\\IslamAlaaEddin\\PycharmProjects\\YoutubeDownloader\\Downloads')  # mst be 2 slashes
output_path_entry.grid(row=1, column=1, padx=8, pady=4)

## search button
search_button = Button(frame, text="Search", command=search_threaded)  # TODO MULTITHREADING
search_button.grid(row=0, column=2, padx=8, pady=8)

## download button
download_button = Button(frame, text="Download", command=download_threaded)  # TODO MULTITHREADING
download_button.grid(row=1, column=2, padx=8, pady=8)

## thumbnail
img = ImageTk.PhotoImage(Image.open("logo.png").resize((196, 196)))
panel = Label(frame, image=img, anchor="w")
panel.grid(row=2, column=0, padx=8, pady=8)

# img.show()


## streams list box
streams_listbox = tkinter.Listbox(frame, selectmode="multiple", width=10, height=12)
streams_listbox.grid(row=2, column=1, padx=8, pady=8, sticky='EW')

# Progress bar widget
download_progress_bar = Progressbar(frame, orient=HORIZONTAL,
                                    length=400, mode='determinate')
download_progress_bar.grid(row=3, column=1, padx=8, pady=8)
download_progress_bar['value'] = 90  # percentage

## cancel downloading button
cancel_downloading_button = Button(frame, text="Abort", command=cancel_download)
cancel_downloading_button.grid(row=3, column=2, padx=8, pady=8)

root.title("Youtube Downloader")
root.mainloop()

from tkinter import Tk
from tkinter import PhotoImage
from tkinter import Frame
from tkinter import Button
from tkinter import Menu
from tkinter import Listbox
from tkinter import Label
from tkinter import Toplevel
from tkinter.ttk import Style
from tkinter.ttk import Scale
from tkinter import filedialog
from mutagen.mp3 import MP3
import pygame
import os
import time
import shutil


def add_songs():
    song_paths = filedialog.askopenfilenames(title="Choose a song",
                                             filetypes=(("mp3 files", "*.mp3"),))
    for song_path in song_paths:
        if song_path.split("/")[-1].replace(".mp3", "") != current_song:
            shutil.copy(song_path, "./music")
    update_list_song()


def get_delete_songs():
    toplevel = Toplevel(master=window)
    list_song = Listbox(master=toplevel,
                        background="black",
                        foreground="green",
                        width=60,
                        selectmode="extended")
    list_song.pack()
    list_song.insert("end", *list_songs)
    Button(master=toplevel,
           text="Delete",
           command=lambda: delete_songs(list_song)).pack()
    update_list_song()


def delete_songs(list_song):
    for i in reversed(list_song.curselection()):
        if list_song.get(i) == current_song:
            refresh()
        os.remove(path=f"./music/{list_song.get(i)}.mp3")
        list_song.delete(i)
    update_list_song()


def update_list_song():
    list_songs.clear()
    for song in os.listdir(path="./music"):
        song = song.replace(".mp3", "")
        list_songs.append(song)
    list_song.delete(0, "end")
    list_song.insert("end", *list_songs)
    for i in range(list_song.size()):
        if current_song == list_song.get(i):
            list_song.selection_set(i)


def refresh():
    global running, current_song
    running = False
    current_song = None
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    list_song.selection_clear("active")
    play_button.configure(image=play_image,
                          command=play)
    status_time.configure(text="00:00 / 00:00")
    status_bar.configure(value=0)


def set_volumn():
    toplevel = Toplevel(master=window)
    volumn_bar = Scale(master=toplevel,
                       from_=0,
                       to=1,
                       value=pygame.mixer.music.get_volume(),
                       command=lambda e: pygame.mixer.music.set_volume(float(volumn_bar.get())))
    volumn_bar.pack()


def select_song(e):
    global running, current_song
    running = True
    play_button.configure(image=pause_image,
                          command=pause)
    song = f"./music/{list_song.get('active')}.mp3"
    pygame.mixer.music.load(filename=song)
    pygame.mixer.music.play(loops=0)
    current_song = list_song.get("active")
    update_status_time()
    update_status_bar()


def play():
    global running, current_song
    if not running:
        running = True
        list_song.selection_clear("active")
        list_song.selection_set(0)
        song = f"./music/{list_songs[0]}.mp3"
        pygame.mixer.music.load(filename=song)
        pygame.mixer.music.play(loops=0)
        current_song = list_songs[0]
    else:
        pygame.mixer.music.unpause()
    play_button.configure(image=pause_image,
                          command=pause)
    update_status_time()
    update_status_bar()


def pause():
    pygame.mixer.music.pause()
    play_button.configure(image=play_image,
                          command=play)


def backward():
    global current_song
    current_song_index = list_song.curselection()[0]
    if current_song_index == 0:
        previous_song_index = list_song.size() - 1
    else:
        previous_song_index = current_song_index - 1
    list_song.selection_clear(current_song_index)
    list_song.selection_set(previous_song_index)
    song = f"./music/{list_song.get(previous_song_index)}.mp3"
    current_song = list_song.get(previous_song_index)
    pygame.mixer.music.load(filename=song)
    pygame.mixer.music.play(loops=0)


def forward():
    global current_song
    current_song_index = list_song.curselection()[0]
    if current_song_index == len(list_songs) - 1:
        next_song_index = 0
    else:
        next_song_index = current_song_index + 1
    list_song.selection_clear(current_song_index)
    list_song.selection_set(next_song_index)
    song = f"./music/{list_song.get(next_song_index)}.mp3"
    current_song = list_song.get(next_song_index)
    pygame.mixer.music.load(filename=song)
    pygame.mixer.music.play(loops=0)
    play_button.configure(image=pause_image,
                          command=pause)


def update_status_time():
    current_time = pygame.mixer.music.get_pos() // 1000
    if pygame.mixer.music.get_pos() != -1:
        song_metagen = MP3(f"./music/{current_song}.mp3")
        song_length = song_metagen.info.length
        length_time = time.strftime("%M:%S", time.gmtime(song_length))
        current_time = time.strftime("%M:%S", time.gmtime(current_time))
        status_time.configure(text=current_time + " / " + length_time)
        status_time.after(500, update_status_time)
    else:
        play_button.configure(image=play_image,
                              command=play)
        if current_song is not None:
            forward()


def update_status_bar():
    current_time = pygame.mixer.music.get_pos() // 1000
    if pygame.mixer.music.get_pos() != -1:
        song_metagen = MP3(f"./music{current_song}.mp3")
        song_length = song_metagen.info.length
        status_bar.configure(to=song_length,
                             value=current_time)
        status_bar.after(500, update_status_bar)


window = Tk()
window.title("Play music application ver-1")
window.configure(background="gray")
window.resizable(width=False,
                 height=False)

backward_image = PhotoImage(file="./image/backward.png")
forward_image = PhotoImage(file="./image/forward.png")
pause_image = PhotoImage(file="./image/pause.png")
play_image = PhotoImage(file="./image/play.png")
running = False
list_songs = []
for i in os.listdir(path="./music"):
    list_songs.append(i.replace(".mp3", ""))
current_song = None
pygame.mixer.init()

menu = Menu(master=window)
option = Menu(master=menu)
option.add_command(label="Add songs",
                   command=add_songs)
option.add_command(label="Delete songs",
                   command=get_delete_songs)
option.add_command(label="Refesh",
                   command=refresh)
option.add_command(label="Volumn",
                   command=set_volumn)
menu.add_cascade(label="Options",
                 menu=option)
window.configure(menu=menu)

list_song = Listbox(master=window,
                    background="black",
                    foreground="green",
                    width=60,
                    selectmode="single")
list_song.pack()
list_song.insert("end", *list_songs)
list_song.bind("<Double-Button-1>", select_song)

status_time = Label(master=window,
                    background="gray",
                    text="00:00 / 00:00",
                    width=50,
                    anchor="e")
status_time.pack()

style = Style()
style.configure("Custom.Horizontal.TScale",
                background="gray",
                state="disbled")
status_bar = Scale(master=window,
                   from_=0,
                   to=100,
                   value=0,
                   length=350,
                   style="Custom.Horizontal.TScale",
                   state="disabled")
status_bar.pack()

frame = Frame(master=window)
frame.pack()

backward_button = Button(master=frame,
                         image=backward_image,
                         command=backward,
                         borderwidth=0,
                         background="gray",
                         activebackground="gray")
play_button = Button(master=frame,
                     image=play_image,
                     command=play,
                     borderwidth=0,
                     background="gray",
                     activebackground="gray")
forward_button = Button(master=frame,
                        image=forward_image,
                        command=forward,
                        borderwidth=0,
                        background="gray",
                        activebackground="gray")
backward_button.grid(row=0,
                     column=0)
play_button.grid(row=0,
                 column=1)
forward_button.grid(row=0,
                    column=2)

window.mainloop()

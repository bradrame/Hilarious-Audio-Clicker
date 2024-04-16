import socket
import tkinter as tk
import threading
from threading import Thread
import os
import random
import mouse
from playsound import playsound
#
# DISCLAIMER: THREAD COUNTS APPEAR QUADROUPLED DUE TO THE MOUSE LISTENER
#
# Initialized sets
id_tag = socket.gethostname()
active_thread = False
audio_folder = 'audio_files'
audio_files = os.listdir(audio_folder)
last_played_file = None
#
#
# Verification processes
def verification_process():
    global active_thread
    print(f'Your computer ID: {id_tag}')
    if os.path.exists('identity'):
        with open('identity', 'r') as file:
            file_content = file.read()
            if id_tag == socket.gethostname() in file_content:
                print(f'Your computer: {id_tag} matches the owner: {socket.gethostname()}')
                active_thread = True
            else:
                print('You aren\'t authorized to use this app.')
                run_button.config(state=tk.DISABLED)
    else:
        with open('identity', 'w') as file:
            file.write(id_tag)
        print('An ID has been created for you')
verification_process()
#
#
# Thread management
def total_threads():
    global thread_count
    active_threads = threading.enumerate()
    thread_count = len(active_threads)
    print(f'Number of threads running: {thread_count}')
def thread_setup():
    if active_thread == True:
        run_button.config(text='Stop', command=thread_kill)
        quit_button.config(state=tk.DISABLED)
        listener_thread = Thread(target=run_listener)
        listener_thread.start()
def thread_kill():
    global active_thread
    active_thread = False
    run_button.config(text='Unleash chaos', command=thread_setup)
    quit_button.config(state=tk.NORMAL)
#
#
# Main operations
def run_listener():
    while active_thread == True:
        mouse.wait('left')
        print('Mouse clicked.')
        play_random_audio()
#
#
# Audio folder operations
def play_random_audio():
    global last_played_file
    if not audio_files:
        print('No audio files found.')
        return
    available_files = [file for file in audio_files if file != last_played_file]
    if not available_files:
        available_files = audio_files.copy()
    audio_file = random.choice(available_files)
    audio_path = os.path.join(audio_folder, audio_file)
    try:
        playsound(audio_path)
        print(f'Played {audio_path}')
        last_played_file = audio_file
    except Exception as e:
        print(f'ERROR: {e}')
        play_random_audio()
#
#
# Tkinter app setup
def quit_app():
    app.quit()
app = tk.Tk()
app.title('Audio Prank Application')
info_label = tk.Label(app, text='\nThis application is designed to\n'
                                'play silly audio files every time\n'
                                'someone clicks the left mouse\n'
                                'button.')
info_label.pack(padx=20, pady=5)
run_button = tk.Button(app, text='Unleash chaos', command=thread_setup)
run_button.pack(pady=15)
quit_button = tk.Button(app, text='Quit', command=quit_app)
quit_button.pack(pady=5)
app.mainloop()
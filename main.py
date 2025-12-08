import tkinter as tk
from tkinter import *
import subprocess
import os
root = tk.Tk()
current_dir = os.path.dirname(os.path.abspath(__file__))

bat_file = os.path.join(current_dir,"zapret-roblox/general.bat")
process = None
def lol():
    process = subprocess.Popen(
        ["cmd.exe", "/c", bat_file],
    creationflags=subprocess.CREATE_NO_WINDOW
    )

def lol1():
    subprocess.run(f"taskkill /F /T /PID {process.}", shell=True)
button = Button(text='lol',command=lol)
button.pack()
button1 = Button(text='lol1',command=lol1)
button1.pack()

root.mainloop()

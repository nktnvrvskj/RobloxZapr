import zapret
import tkinter as tk
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        " ".join(sys.argv),
        None,
        1
    )
    sys.exit(0)

if not is_admin():
    restart_as_admin()


root = tk.Tk()
root.geometry("300x300")
root.title("Roblox Zapr")

def start():
    zapret.start()
    button.config(text="stop",command=stop)


def stop():
    zapret.stop()
    button.config(text="Start",command=start)


button = tk.Button(root, text="Start", command=start)
button.pack()

root.mainloop()
stop()

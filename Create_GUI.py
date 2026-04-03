# p227_command_gui.py
# Project 2.2.7 - Creating a Command Line GUI

import subprocess
import tkinter as tk
import tkinter.scrolledtext as tksc
from tkinter.filedialog import asksaveasfilename
import platform


def mSave():
    filename = asksaveasfilename(
        defaultextension='.txt',
        filetypes=[('Text files', '*.txt'), ('All files', '*.*')]
    )
    if filename is None:
        return
    file = open(filename, mode='w')
    text_to_save = command_textbox.get("1.0", tk.END)
    file.write(text_to_save)
    file.close()


def do_command(command):
    global command_textbox, url_entry

    url_val = url_entry.get()
    if len(url_val) == 0:
        url_val = "::1"

    command_textbox.delete(1.0, tk.END)
    command_textbox.insert(tk.END, command + " " + url_val + " working....\n")
    command_textbox.update()

    os_name = platform.system()
    if command == "ping":
        full_cmd = "ping " + url_val if os_name == "Windows" else "ping -c 4 " + url_val
    elif command == "tracert":
        full_cmd = "tracert " + url_val if os_name == "Windows" else "traceroute " + url_val
    elif command == "nslookup":
        full_cmd = "nslookup " + url_val
    else:
        full_cmd = command + " " + url_val

    try:
        with subprocess.Popen(
            full_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        ) as p:
            for line in p.stdout:
                command_textbox.insert(tk.END, line)
                command_textbox.update()
    except Exception as e:
        command_textbox.insert(tk.END, "Error: " + str(e) + "\n")


# Window setup
root = tk.Tk()
root.title("Network Tools")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# URL input
url_label = tk.Label(frame, text="Enter Domain or IP:")
url_label.pack(anchor="w")

url_entry = tk.Entry(frame, width=50, font=("Arial", 11))
url_entry.insert(0, "www.pltw.org")
url_entry.pack(pady=(0, 10))

# Buttons
ping_btn = tk.Button(frame, text="Check if URL is up (Ping)",
    command=lambda: do_command("ping"),
    font=("Arial", 10), width=30, bg="#d0e8ff", cursor="hand2")
ping_btn.pack(pady=3)

tracert_btn = tk.Button(frame, text="Trace Network Path (Traceroute)",
    command=lambda: do_command("tracert"),
    font=("Arial", 10), width=30, bg="#d0ffd8", cursor="hand2")
tracert_btn.pack(pady=3)

nslookup_btn = tk.Button(frame, text="Look Up DNS Info (NSLookup)",
    command=lambda: do_command("nslookup"),
    font=("Arial", 10), width=30, bg="#fff3d0", cursor="hand2")
nslookup_btn.pack(pady=3)

save_btn = tk.Button(frame, text="Save Results to File",
    command=mSave,
    font=("Arial", 10), width=30, bg="#eeeeee", cursor="hand2")
save_btn.pack(pady=(10, 5))

# Output box
command_textbox = tksc.ScrolledText(frame, height=18, width=70, font=("Courier New", 10))
command_textbox.pack(pady=(8, 0))

root.mainloop()
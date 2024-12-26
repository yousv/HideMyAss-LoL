import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
import os

def check_status():
    try:
        result = subprocess.run('netsh advfirewall firewall show rule name="lolchat"',
                              capture_output=True, text=True, shell=True)
        return "No rules match the specified criteria." not in result.stdout
    except:
        return False

def set_offline():
    try:
        subprocess.run('netsh advfirewall firewall add rule name="lolchat" '
                      'dir=out remoteport=5223 protocol=TCP action=block',
                      shell=True, check=True)
        update_status()
    except:
        messagebox.showerror("Error", "Failed to set offline status")

def set_online():
    try:
        subprocess.run('netsh advfirewall firewall delete rule name="lolchat"',
                      shell=True, check=True)
        update_status()
    except:
        messagebox.showerror("Error", "Failed to set online status")

def update_status():
    if check_status():
        status_label.configure(text="Status: OFFLINE", foreground="#F7768E")
    else:
        status_label.configure(text="Status: ONLINE", foreground="#9ECE6A")

# Setup window
root = tk.Tk()
root.title("LoL Status Manager")
root.geometry("300x180")
root.resizable(False, False)

# Set icon
if getattr(sys, 'frozen', False):
    icon_path = os.path.join(sys._MEIPASS, "app.ico")
else:
    icon_path = "app.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Colors
COLORS = {
    'bg': "#1A1B26",
    'button': "#24283B",
    'button_hover': "#414868",
    'text': "#A9B1D6"
}

# Configure styles
root.configure(bg=COLORS['bg'])
style = ttk.Style()
style.theme_use('default')

for item in ['TFrame', 'TLabel', 'TButton']:
    style.configure(item, background=COLORS['bg'], foreground=COLORS['text'])

style.configure('TButton', padding=5, font=('Segoe UI', 10))
style.map('TButton',
          background=[('active', COLORS['button_hover'])],
          foreground=[('active', COLORS['text'])])

# Create widgets
frame = ttk.Frame(root)
frame.pack(expand=True, fill='both', padx=15, pady=15)

status_label = ttk.Label(frame, text="Checking status...", font=('Segoe UI', 11))
status_label.pack(pady=10)

ttk.Button(frame, text="Appear Offline", command=set_offline).pack(fill='x', pady=4)
ttk.Button(frame, text="Appear Online", command=set_online).pack(fill='x', pady=4)

# Initial status check
update_status()

# Start app
root.mainloop()

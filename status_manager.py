import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import logging
import os
import sys
from typing import Optional

class FirewallManager:
    RULE_NAME = "lolchat"
    CHAT_PORT = "5223"
    
    @staticmethod
    def check_rule_exists() -> bool:
        try:
            result = subprocess.run(
                f'netsh advfirewall firewall show rule name="{FirewallManager.RULE_NAME}"',
                capture_output=True,
                text=True,
                shell=True,
                check=True
            )
            return "No rules match the specified criteria." not in result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking firewall rule: {e}")
            return False

    @staticmethod
    def add_block_rule() -> bool:
        try:
            subprocess.run(
                f'netsh advfirewall firewall add rule '
                f'name="{FirewallManager.RULE_NAME}" '
                f'dir=out remoteport={FirewallManager.CHAT_PORT} '
                f'protocol=TCP action=block',
                shell=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Error adding firewall rule: {e}")
            return False

    @staticmethod
    def remove_rule() -> bool:
        try:
            subprocess.run(
                f'netsh advfirewall firewall delete rule name="{FirewallManager.RULE_NAME}"',
                shell=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Error removing firewall rule: {e}")
            return False

class StatusManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.firewall = FirewallManager()
        self.update_status()

    def setup_window(self):
        self.root.title("Hide My Ass LoL")
        self.root.geometry("320x200")
        self.root.resizable(False, False)
        
        # Set the window and taskbar icon
        if getattr(sys, 'frozen', False):
            # If running as exe (PyInstaller)
            application_path = sys._MEIPASS
        else:
            # If running as script
            application_path = os.path.dirname(os.path.abspath(__file__))
            
        icon_path = os.path.join(application_path, "app.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
            
        self.configure_styles()

    def configure_styles(self):
        self.colors = {
            'bg': "#1A1B26",
            'button_bg': "#24283B",
            'button_hover': "#414868",
            'text': "#A9B1D6",
            'online': "#9ECE6A",
            'offline': "#F7768E",
            'frame_bg': "#1F2335"
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure("TFrame",
                       background=self.colors['frame_bg'])
        
        style.configure("Offline.TButton",
                       background=self.colors['button_bg'],
                       foreground=self.colors['text'],
                       padding=(10, 5),
                       font=('Segoe UI', 10))
                       
        style.configure("Online.TButton",
                       background=self.colors['button_bg'],
                       foreground=self.colors['text'],
                       padding=(10, 5),
                       font=('Segoe UI', 10))
        
        style.map("Offline.TButton",
                 background=[("active", self.colors['button_hover'])],
                 foreground=[("active", self.colors['text'])])
                 
        style.map("Online.TButton",
                 background=[("active", self.colors['button_hover'])],
                 foreground=[("active", self.colors['text'])])
        
        style.configure("Status.TLabel",
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 11),
                       padding=10)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(expand=True, fill='both', padx=15, pady=15)

        self.status_label = ttk.Label(
            main_frame,
            text="Checking status...",
            style='Status.TLabel'
        )
        self.status_label.pack(pady=10)

        btn_frame = ttk.Frame(main_frame, style="TFrame")
        btn_frame.pack(fill='x', pady=5)

        ttk.Button(
            btn_frame,
            text="Appear Offline",
            command=self.set_offline,
            style='Offline.TButton'
        ).pack(fill='x', pady=4)

        ttk.Button(
            btn_frame,
            text="Appear Online",
            command=self.set_online,
            style='Online.TButton'
        ).pack(fill='x', pady=4)

    def update_status(self):
        if FirewallManager.check_rule_exists():
            self.status_label.configure(text="Status: OFFLINE", 
                                      foreground=self.colors['offline'])
        else:
            self.status_label.configure(text="Status: ONLINE", 
                                      foreground=self.colors['online'])

    def set_offline(self):
        if FirewallManager.add_block_rule():
            self.update_status()
        else:
            self.show_error("Failed to set offline status")

    def set_online(self):
        if FirewallManager.remove_rule():
            self.update_status()
        else:
            self.show_error("Failed to set online status")

    def show_error(self, message: str):
        messagebox.showerror("Error", message)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    app = StatusManagerApp()
    app.run()
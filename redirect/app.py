import tkinter as tk
from tkinter import ttk
import subprocess
import os

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Page")
        self.root.geometry("400x300")
        self.root.configure(bg="#2e2e2e")

        # Stijlen
        self.style = ttk.Style()
        self.style.configure("TButton", background="#4CAF50", foreground="#000000", font=("Helvetica", 12))
        
        # Welkomstlabel
        self.welcome_label = ttk.Label(root, text="Welcome! Choose an option:", background="#2e2e2e", foreground="#ffffff", font=("Helvetica", 14))
        self.welcome_label.pack(pady=20)

        # Knoppen
        self.file_deleter_button = ttk.Button(root, text="File Deleter", command=self.open_file_deleter)
        self.file_deleter_button.pack(pady=10)

        self.shooter_game_button = ttk.Button(root, text="Shooter Game", command=self.open_shooter_game)
        self.shooter_game_button.pack(pady=10)

        self.mario_game_button = ttk.Button(root, text="Mario", command=self.open_mario_game)
        self.mario_game_button.pack(pady=10)

    def open_file_deleter(self):
        self.run_script("file.py")

    def open_shooter_game(self):
        self.run_script("shooter.py")

    def open_mario_game(self):
        self.run_script("mario.py")

    def run_script(self, script_name):
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        subprocess.Popen(["python", script_path])

if __name__ == "__main__":
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()

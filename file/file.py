import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math
import subprocess

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.root.geometry("800x600")
        self.root.configure(bg="#2e2e2e")

        # Hoofd frame met scrollbar
        self.main_frame = tk.Frame(root, bg="#2e2e2e")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg="#2e2e2e")
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2e2e2e")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Stijlen
        self.style = ttk.Style()
        self.style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Helvetica", 12))
        self.style.configure("TButton", background="#4CAF50", foreground="#000000", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12))
        self.style.configure("Treeview", background="#424242", foreground="#ffffff", fieldbackground="#424242", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", background="#4CAF50", foreground="#ffffff", font=("Helvetica", 14))
        
        # Layout configureren
        self.scrollable_frame.columnconfigure(0, weight=1)

        # Path invoer
        self.path_label = ttk.Label(self.scrollable_frame, text="Directory Path:")
        self.path_label.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(self.scrollable_frame, textvariable=self.path_var)
        self.path_entry.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        
        self.browse_button = ttk.Button(self.scrollable_frame, text="Apply", command=self.update_file_list)
        self.browse_button.grid(row=2, column=0, sticky='ew', padx=5, pady=5)

        # Zoekbalk label
        self.search_label = ttk.Label(self.scrollable_frame, text="Search:")
        self.search_label.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
        
        # Zoekbalk
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.update_file_list)
        self.search_entry = ttk.Entry(self.scrollable_frame, textvariable=self.search_var)
        self.search_entry.grid(row=4, column=0, sticky='ew', padx=5, pady=5)
        
        # Datumfilter label
        self.date_filter_label = ttk.Label(self.scrollable_frame, text="Date Filter (YYYY or YYYY-MM or YYYY-MM-DD):")
        self.date_filter_label.grid(row=5, column=0, sticky='ew', padx=5, pady=5)
        
        # Datumfilter
        self.date_filter_var = tk.StringVar()
        self.date_filter_var.trace_add('write', self.update_file_list)
        self.date_filter_entry = ttk.Entry(self.scrollable_frame, textvariable=self.date_filter_var)
        self.date_filter_entry.grid(row=6, column=0, sticky='ew', padx=5, pady=5)

        # Groottefilter label
        self.size_filter_label = ttk.Label(self.scrollable_frame, text="Size Filter (KB, MB, GB):")
        self.size_filter_label.grid(row=7, column=0, sticky='ew', padx=5, pady=5)

        # Groottefilter
        self.size_filter_var = tk.StringVar()
        self.size_filter_var.trace_add('write', self.update_file_list)
        self.size_filter_entry = ttk.Entry(self.scrollable_frame, textvariable=self.size_filter_var)
        self.size_filter_entry.grid(row=8, column=0, sticky='ew', padx=5, pady=5)

        # Specifieke grootte filter label
        self.specific_size_filter_label = ttk.Label(self.scrollable_frame, text="Specific Size Filter (e.g., 300KB):")
        self.specific_size_filter_label.grid(row=9, column=0, sticky='ew', padx=5, pady=5)

        # Specifieke grootte filter
        self.specific_size_filter_var = tk.StringVar()
        self.specific_size_filter_var.trace_add('write', self.update_file_list)
        self.specific_size_filter_entry = ttk.Entry(self.scrollable_frame, textvariable=self.specific_size_filter_var)
        self.specific_size_filter_entry.grid(row=10, column=0, sticky='ew', padx=5, pady=5)

        # Frame voor Treeview en scrollbars
        self.tree_frame = ttk.Frame(self.scrollable_frame)
        self.tree_frame.grid(row=11, column=0, pady=20, sticky='nsew')

        self.scrollable_frame.rowconfigure(11, weight=1)
        
        self.tree_scroll_y = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL)
        self.tree_scroll_x = ttk.Scrollbar(self.scrollable_frame, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("name", "path", "size", "date"), show="headings",
                                 yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)
        self.tree.heading("name", text="Name")
        self.tree.heading("path", text="Path")
        self.tree.heading("size", text="Size")
        self.tree.heading("date", text="Date Modified")
        self.tree.column("name", width=150)
        self.tree.column("path", width=250)
        self.tree.column("size", width=100)
        self.tree.column("date", width=150)

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_scroll_x.grid(row=12, column=0, sticky='ew')

        # Knoppen
        self.button_frame = ttk.Frame(self.scrollable_frame)
        self.button_frame.grid(row=13, column=0, pady=5, sticky='ew')

        self.delete_button = ttk.Button(self.button_frame, text="Delete Selected", command=self.delete_selected)
        self.delete_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.open_location_button = ttk.Button(self.button_frame, text="Open File Location", command=self.open_file_location)
        self.open_location_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.open_file_button = ttk.Button(self.button_frame, text="Open File", command=self.open_file)
        self.open_file_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        self.button_frame.columnconfigure([0, 1, 2], weight=1)

        # Extensie filter
        self.filter_label = ttk.Label(self.scrollable_frame, text="Filter by extension:")
        self.filter_label.grid(row=14, column=0, sticky='ew', padx=5, pady=5)
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add('write', self.update_file_list)
        self.filter_entry = ttk.Entry(self.scrollable_frame, textvariable=self.filter_var)
        self.filter_entry.grid(row=15, column=0, sticky='ew', padx=5, pady=5)

    def update_file_list(self, *args):
        search_term = self.search_var.get().lower()
        file_extension = self.filter_var.get().lower()
        date_filter = self.date_filter_var.get()
        size_filter = self.size_filter_var.get().upper()
        specific_size_filter = self.specific_size_filter_var.get().upper()
        directory = self.path_var.get()

        self.tree.delete(*self.tree.get_children())

        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory path")
            return

        date_filter_len = len(date_filter)

        files_found = False
        for root, dirs, files in os.walk(directory):
            for file in files:
                if search_term in file.lower() and (not file_extension or file.lower().endswith(file_extension)):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    file_size_str = self.convert_size(file_size)
                    file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
                    file_date_str = file_date.strftime('%Y-%m-%d %H:%M:%S')

                    if date_filter_len == 4:  # Alleen jaar
                        if file_date.strftime('%Y') != date_filter:
                            continue
                    elif date_filter_len == 7:  # Jaar en maand
                        if file_date.strftime('%Y-%m') != date_filter:
                            continue
                    elif date_filter_len == 10:  # Volledige datum
                        if file_date.strftime('%Y-%m-%d') != date_filter:
                            continue

                    if size_filter and not file_size_str.endswith(size_filter):
                        continue

                    if specific_size_filter:
                        specific_size_bytes = self.parse_size(specific_size_filter)
                        specific_size_str = self.convert_size(specific_size_bytes).split()[0]
                        if not file_size_str.startswith(specific_size_str):
                            continue

                    self.tree.insert("", tk.END, values=(file, file_path, file_size_str, file_date_str))
                    files_found = True

        if not files_found:
            self.tree.insert("", tk.END, values=("No files found", "", "", ""))

    def size_filter_match(self, file_size, size_filter):
        size_filter = size_filter.strip()
        if size_filter.startswith('>'):
            size = self.parse_size(size_filter[1:])
            return file_size > size
        elif size_filter.startswith('<'):
            size = self.parse_size(size_filter[1:])
            return file_size < size
        else:
            return True

    def parse_size(self, size_str):
        size_str = size_str.strip().upper()
        if size_str.endswith('KB'):
            return float(size_str[:-2]) * 1024
        elif size_str.endswith('MB'):
            return float(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('GB'):
            return float(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            return float(size_str)

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            file_path = self.tree.item(selected_item[0], 'values')[1]
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            total, used, free = shutil.disk_usage("/")
            free_space_before = free / (1024 * 1024 * 1024)
            free_space_after = (free + file_size) / (1024 * 1024 * 1024)
            
            try:
                os.remove(file_path)
                messagebox.showinfo("Success", f"File {file_path} deleted successfully.\n\n"
                                              f"File Size: {file_size_mb:.2f} MB\n"
                                              f"Free Space Before: {free_space_before:.2f} GB\n"
                                              f"Free Space After: {free_space_after:.2f} GB")
                self.update_file_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file {file_path}. Error: {e}")
        else:
            messagebox.showwarning("No selection", "Please select a file to delete.")

    def open_file_location(self):
        selected_item = self.tree.selection()
        if selected_item:
            file_path = self.tree.item(selected_item[0], 'values')[1]
            if os.path.isfile(file_path):
                subprocess.Popen(f'explorer /select,"{file_path}"')
            else:
                messagebox.showerror("Error", "Selected path is not a file.")
        else:
            messagebox.showwarning("No selection", "Please select a file to open location.")

    def open_file(self):
        selected_item = self.tree.selection()
        if selected_item:
            file_path = self.tree.item(selected_item[0], 'values')[1]
            if os.path.isfile(file_path):
                try:
                    os.startfile(file_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open file {file_path}. Error: {e}")
            else:
                messagebox.showerror("Error", "Selected path is not a file.")
        else:
            messagebox.showwarning("No selection", "Please select a file to open.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()

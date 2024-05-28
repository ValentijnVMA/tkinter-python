import os
import tkinter as tk
from tkinter import ttk, messagebox

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.root.geometry("800x600")
        self.root.configure(bg="#2e2e2e")
        
        # Stijlen
        self.style = ttk.Style()
        self.style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Helvetica", 12))
        self.style.configure("TButton", background="#4CAF50", foreground="#000000", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12))
        self.style.configure("Treeview", background="#424242", foreground="#ffffff", fieldbackground="#424242", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", background="#4CAF50", foreground="#ffffff", font=("Helvetica", 14))
        
        # Path invoer
        self.path_label = ttk.Label(root, text="Directory Path:")
        self.path_label.pack(pady=5)
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(root, textvariable=self.path_var, width=50)
        self.path_entry.pack(pady=5)
        
        self.browse_button = ttk.Button(root, text="Browse", command=self.update_file_list)
        self.browse_button.pack(pady=5)

        # Zoekbalk label
        self.search_label = ttk.Label(root, text="Search:")
        self.search_label.pack(pady=5)
        
        # Zoekbalk
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.update_file_list)
        self.search_entry = ttk.Entry(root, textvariable=self.search_var, width=50)
        self.search_entry.pack(pady=10)
        
        # Bestanden lijst
        self.tree = ttk.Treeview(root, columns=("name", "path"), show="headings")
        self.tree.heading("name", text="Name")
        self.tree.heading("path", text="Path")
        self.tree.column("name", width=200)
        self.tree.column("path", width=400)
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Verwijder knop
        self.delete_button = ttk.Button(root, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(pady=10)

        # Extensie filter
        self.filter_label = ttk.Label(root, text="Filter by extension:")
        self.filter_label.pack(pady=5)
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add('write', self.update_file_list)
        self.filter_entry = ttk.Entry(root, textvariable=self.filter_var, width=20)
        self.filter_entry.pack(pady=5)

    def update_file_list(self, *args):
        search_term = self.search_var.get().lower()
        file_extension = self.filter_var.get().lower()
        directory = self.path_var.get()

        self.tree.delete(*self.tree.get_children())

        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory path")
            return

        for root, dirs, files in os.walk(directory):
            for file in files:
                if search_term in file.lower() and (not file_extension or file.lower().endswith(file_extension)):
                    self.tree.insert("", tk.END, values=(file, os.path.join(root, file)))

    def delete_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            file_path = self.tree.item(selected_item[0], 'values')[1]
            try:
                os.remove(file_path)
                messagebox.showinfo("Success", f"File {file_path} deleted successfully.")
                self.update_file_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file {file_path}. Error: {e}")
        else:
            messagebox.showwarning("No selection", "Please select a file to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()

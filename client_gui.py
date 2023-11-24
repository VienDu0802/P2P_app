# client_gui.py
import tkinter as tk
from tkinter import messagebox
from client import FileClient

def connect_to_server():
    try:
        client.connect_to_server()
        label_status.config(text="Connected to server.")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))
        label_status.config(text="Failed to connect to server.")

def discover_files():
    try:
        hostname = entry_hostname.get()
        files = client.discover_files(hostname)
        label_files.config(text=str(files))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def publish_file():
    try:
        filename = entry_filename.get()
        client.publish_file(filename)
        label_status.config(text=f"Published file: {filename}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

client = FileClient()

root = tk.Tk()
root.title("Client Management")

frame = tk.Frame(root)
frame.pack(pady=10)

entry_hostname = tk.Entry(frame, width=50)
entry_hostname.pack(side=tk.LEFT, padx=5)

button_discover = tk.Button(frame, text="Discover Files", command=discover_files)
button_discover.pack(side=tk.LEFT, padx=5)

entry_filename = tk.Entry(frame, width=50)
entry_filename.pack(side=tk.LEFT, padx=5)

button_publish = tk.Button(frame, text="Publish File", command=publish_file)
button_publish.pack(side=tk.LEFT, padx=5)

label_files = tk.Label(root, text="Files will be listed here...")
label_files.pack(pady=5)

label_status = tk.Label(root, text="Status will be shown here...")
label_status.pack(pady=5)

# Kết nối đến server khi khởi động ứng dụng
connect_to_server()

root.mainloop()

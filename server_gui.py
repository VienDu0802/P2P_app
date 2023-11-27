import tkinter as tk
from tkinter import messagebox
import threading
import queue
from server import FileServer

class ServerGUI:
    def __init__(self, master):
        self.master = master
        self.server = None
        self.server_thread = None
        self.update_thread = None
        self.client_repo_files_thread = None
        master.title("Server Management")

        sidebar = tk.Frame(master, bg="gray", width=200)
        sidebar.pack(side="left", fill="y", expand=False)

        label = tk.Label(sidebar, text="SERVER SIDE", bg="lightblue", fg="black", font=("Arial", 20), relief="ridge", borderwidth=2)
        label.pack(pady=20, padx=16)

        self.start_button = tk.Button(sidebar, text="Start Server", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1, command=self.start_server)
        self.start_button.pack(pady=(10, 20), padx=2, ipady=4)

        self.stop_button = tk.Button(sidebar, text="Stop Server", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1, command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=(10, 20), padx=2, ipady=4)

        quit_button = tk.Button(sidebar, text="QUIT", bg="red", fg="white", width=12, font=("Arial", 11), height=1, command=master.destroy)
        quit_button.pack(side="bottom", pady=(10, 40), padx=2, ipady=4)

        content_Wrapper = tk.Frame(master, bg="lightgray")
        content_Wrapper.pack(side="right", fill="both", expand=True)

        client_list_label = tk.Label(content_Wrapper, text="Client List", font=("Arial", 16), bg="lightgray")
        client_list_label.pack(side="top", pady=5)

        self.client_list_box = tk.Listbox(content_Wrapper, height=20, width=50)
        self.client_list_box.config(font=("Arial", 13))
        self.client_list_box.pack(side="top", fill="both", expand=True)

        self.cli_input = tk.Entry(content_Wrapper, bd=3, font=("Arial", 13))
        self.cli_input.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        enter_button = tk.Button(content_Wrapper, text="Enter", font=("Arial", 13), height=1, command=self.execute_cli_command)
        enter_button.pack(side="left", padx=10, pady=10, ipadx=20)

        self.client_list_queue = queue.Queue()

    def execute_cli_command(self):
        command = self.cli_input.get()
        if command.startswith("ping"):
            self.ping_client(command)
        self.cli_input.delete(0, tk.END)

    def ping_client(self, command):
        try:
            _, client_address = command.split(" ")
            host, port_str = client_address.split(":")
            port = int(port_str)
            client_key = (host, port)

            if client_key in self.server.clients and self.server.clients[client_key]['connected']:
                messagebox.showinfo("Ping Result", f"Client {client_address} is connected.")
            else:
                messagebox.showinfo("Ping Result", f"Client {client_address} is not connected.")
        except ValueError:
            messagebox.showerror("Error", "Invalid command format. Use 'ping ip:port'.")

    def update_client_list(self):
        while True:
            try:
                client_list = self.client_list_queue.get_nowait()
                self.client_list_box.delete(0, tk.END)
                for client_address, client_info in client_list:
                    ip, port = client_address
                    status = "Connected" if client_info['connected'] else "Disconnected"
                    client_label = f"{ip}:{port} - {status}"
                    self.client_list_box.insert(tk.END, client_label)
            except queue.Empty:
                break

    def receive_client_repo_files(self):
        while True:
            try:
                repo_files = self.server.client_repo_files_queue.get_nowait()
                self.display_client_repo_files(repo_files)
            except queue.Empty:
                break

    def display_client_repo_files(self, repo_files):
        repo_window = tk.Toplevel()
        repo_window.title("Client Repository Files")

        file_listbox = tk.Listbox(repo_window, height=10, width=40)
        file_listbox.pack()

        for file_name in repo_files:
            file_listbox.insert(tk.END, file_name)

        close_button = tk.Button(repo_window, text="Close", command=repo_window.destroy)
        close_button.pack()

    def start_server(self):
        if self.server is None:
            self.server = FileServer()
            self.server_thread = threading.Thread(target=self.server.accept_connections)
            self.server_thread.daemon = True
            self.server_thread.start()
            self.update_thread = threading.Thread(target=self.update_client_list)
            self.update_thread.daemon = True
            self.update_thread.start()
            self.client_repo_files_thread = threading.Thread(target=self.receive_client_repo_files)
            self.client_repo_files_thread.daemon = True
            self.client_repo_files_thread.start()
            self.start_button.config(bg="lightgreen", fg="black", state=tk.DISABLED)
            self.stop_button.config(bg="lightgray", state=tk.NORMAL)
    
    def stop_server(self):
        if self.server is not None:
            self.server.shutdown_server()
            self.server_thread.join()
            self.server = None
            self.update_thread.join()
            self.client_repo_files_thread.join()
            self.start_button.config(bg="lightgray", state=tk.NORMAL)
            self.stop_button.config(bg="red", state=tk.DISABLED)
    
    def on_closing(self):
        if self.server is not None:
            self.server.shutdown_server()
            self.server_thread.join()
            self.update_thread.join()
            self.client_repo_files_thread.join()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    server_gui = ServerGUI(root)
    root.protocol("WM_DELETE_WINDOW", server_gui.on_closing)
    root.mainloop()

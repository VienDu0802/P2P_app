import tkinter as tk
from server import FileServer
import threading

class ServerGUI:
    def __init__(self, master):
        self.master = master
        self.server = None
        self.server_thread = None
        master.title("Server Management")

        # Tạo sidebar
        sidebar = tk.Frame(master, bg="gray", width=200)
        sidebar.pack(side="left", fill="y", expand=False)

        label = tk.Label(sidebar, text="SERVER SIDE", bg="lightblue", fg="black", font=("Arial", 20), relief="ridge", borderwidth=2)
        label.pack(pady=20, padx=16)

        # Nút Start Server
        self.start_button = tk.Button(sidebar, text="Start Server", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1, command=self.start_server)
        self.start_button.pack(pady=(10, 20), padx=2, ipady=4)

        # Nút Stop Server
        self.stop_button = tk.Button(sidebar, text="Stop Server", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1, command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=(10, 20), padx=2, ipady=4)

        # Nút Quit
        quit_button = tk.Button(sidebar, text="QUIT", bg="red", fg="white", width=12, font=("Arial", 11), height=1, command=master.destroy)
        quit_button.pack(side="bottom", pady=(10, 40), padx=2, ipady=4)

         # Content Wrapper
        content_Wrapper = tk.Frame(master, bg="lightgray")
        content_Wrapper.pack(side="right", fill="both", expand=True)

        # Nhãn "Client List"
        client_list_label = tk.Label(content_Wrapper, text="Client List", font=("Arial", 16), bg="lightgray")
        client_list_label.pack(side="top", pady=5)

        # Content - Danh sách client
        self.client_list_box = tk.Listbox(content_Wrapper, height=20, width=50)
        self.client_list_box.config(font=("Arial", 13))
        self.client_list_box.pack(side="top", fill="both", expand=True)

        # CLI
        cli = tk.Frame(content_Wrapper, bg="lightgray", height=50)
        cli.pack(side="bottom", fill="x", expand=False, padx=50, pady=10)

        cli_input = tk.Entry(cli, bd=3, font=("Arial", 13))
        cli_input.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        enter_button = tk.Button(cli, text="Enter", font=("Arial", 13), height=1)
        enter_button.pack(side="left", padx=10, pady=10, ipadx=20)

    def start_server(self):
        if self.server is None:
            self.server = FileServer()
            self.server_thread = threading.Thread(target=self.server.accept_connections)
            self.server_thread.daemon = True
            self.server_thread.start()
            self.start_button.config(bg="lightgreen",fg="black", state=tk.DISABLED)
            self.stop_button.config(bg="lightgray", state=tk.NORMAL)
        self.update_client_list()

    def update_client_list(self):
        if self.server:
            client_list = self.server.get_client_list()
            self.client_list_box.delete(0, tk.END)
            for client in client_list:
                self.client_list_box.insert(tk.END, client)

    def stop_server(self):
        if self.server is not None:
            self.server.shutdown_server()
            self.server_thread.join()
            self.server = None
            self.start_button.config(bg="lightgray", state=tk.NORMAL)
            self.stop_button.config(bg="red", state=tk.DISABLED)

    def on_closing(self):
        if self.server is not None:
            self.server.shutdown_server()
            self.server_thread.join()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    server_gui = ServerGUI(root)
    root.protocol("WM_DELETE_WINDOW", server_gui.on_closing)
    root.mainloop()

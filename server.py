import socket
import threading
import cmd
from tkinter import messagebox
import queue
import os

class FileServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is running on IP: {self.host}, Port: {self.port}")
        self.clients = {}
        self.running = True
        self.repo_base_path = "D:\\Mang_MT\\BTL\\MyApp_Demo"
        self.client_repo_files_queue = queue.Queue()

    def accept_connections(self):
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"Connection from {address} has been established.")
                self.clients[address] = {'socket': client_socket, 'connected': True}
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
                client_handler.start()
            except OSError:
                break
        print(f"Current clients: {self.clients}")

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                command = client_socket.recv(1024).decode('utf-8')
                if command:
                    print(f"Received command from {client_address}: {command}")  # Thêm dòng in này để kiểm tra lệnh nhận được từ client
                    if command.startswith("ping"):
                        if self.clients[client_address]['connected']:
                            messagebox.showinfo("Ping", "This client is still connected to the server")
                        else:
                            messagebox.showinfo("Ping", "This client is not connected to the server")
                    elif command == 'discover':
                        connected_clients = ', '.join([str(addr) for addr, info in self.clients.items() if info['connected']])
                        print(f"Sending list of connected clients to {client_address}: {connected_clients}")  # Thêm dòng in này để kiểm tra việc gửi danh sách client
                        client_socket.send(f"Connected Clients: {connected_clients}".encode('utf-8'))
                        # Gửi danh sách client thông qua queue
                        self.client_list_queue.put(connected_clients)
                    else:
                        # Xử lý các lệnh khác
                        pass
            except:
                self.clients[client_address]['connected'] = False
                print(f"Client {client_address} disconnected. Updated clients: {self.clients}")
                
                # Update the client list box
                self.update_client_list()

    def get_client_list(self):
        client_list = []
        for client_address, client_info in self.clients.items():
            client_status = "Connected" if client_info['connected'] else "Disconnected"
            client_list.append(f"{client_address[0]}:{client_address[1]} - {client_status}")
        return client_list

    def update_client_list(self):
        client_list = self.get_client_list()
        self.update_queue.put(client_list)

    def send_client_repo_files(self, client_socket, client_address):
        try:
            client_repo_path = os.path.join(self.repo_base_path, str(client_address))
            if os.path.exists(client_repo_path):
                repo_files = os.listdir(client_repo_path)
                client_socket.send("Repo Files:\n".encode('utf-8'))
                for file_name in repo_files:
                    client_socket.send(f"{file_name}\n".encode('utf-8'))
                self.client_repo_files_queue.put(repo_files)
            else:
                client_socket.send("Repo not found.\n".encode('utf-8'))
        except Exception as e:
            print(f"Error sending repo files to {client_address}: {e}")

    def ping_client(self, client_info):
        try:
            host, port_str = client_info.split(":")
            port = int(port_str)
            client_key = (host, port)

            if client_key in self.clients:
                client_socket = self.clients[client_key]['socket']
                client_socket.send("ping".encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                print(f"Response from client {client_info}: {response}")
            else:
                print(f"No client found at {client_info}.")
        except ValueError:
            print("Invalid address format. Use 'host:port'.")

    def discover_clients(self):
        connected_clients = ', '.join([str(addr) for addr, info in self.clients.items() if info['connected']])
        print(f"Connected Clients: {connected_clients}")

    def shutdown_server(self):
        self.running = False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
            except ConnectionRefusedError:
                pass
        self.server_socket.close()
        print("Server has been shut down.")

class ServerCLI(cmd.Cmd):
    prompt = "> "

    def __init__(self, server):
        super().__init__()
        self.server = server
        self.server.update_queue = queue.Queue()

    def cmdloop(self):
        while True:
            try:
                client_list = self.server.update_queue.get()
                self.update_gui_client_list(client_list)
                super().cmdloop()
            except KeyboardInterrupt:
                print("Shutting down the server via KeyboardInterrupt.")
                self.server.shutdown_server()
                break

    def default(self, line):
        self.server.execute_cli_command(line)

    def do_ping(self, arg):
        print(f"Executing ping command for: {arg}")
        try:
            host, port_str = arg.split(":")
            port = int(port_str)
            client_key = (host, port)

            print(f"Checking client at {client_key}")

            if client_key in self.server.clients:
                status = "connected" if self.server.clients[client_key]['connected'] else "not connected"
                print(f"Client {arg} is {status}.")
            else:
                print(f"No client found at {arg}.")
        except ValueError:
            print("Invalid address format. Use 'host:port'.")


if __name__ == "__main__":
    server = FileServer()
    server_thread = threading.Thread(target=server.accept_connections)
    server_thread.start()

    cli = ServerCLI(server)
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("Shutting down the server via KeyboardInterrupt.")
        server.shutdown_server()
        server_thread.join()

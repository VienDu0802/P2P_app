import socket
import threading
import cmd
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
        self.clients_info = {}
        self.running = True
        self.server_repo_path = "D:\Mang_MT\BTL\MyApp_Demo"
    
    def start(self):
        print("Server is starting...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connected to client: {client_address[0]}:{client_address[1]}")
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def get_client_list(self):
        client_list = set()
        server_data_file_path = os.path.join(self.server_repo_path, 'Server_Data.txt')
        try:
            with open(server_data_file_path, 'r') as server_data_file:
                for line in server_data_file:
                    _, client_ip = line.strip().split(" - ")
                    client_list.add(client_ip)
        except FileNotFoundError:
            print("Server data file not found.")
        return list(client_list)

    def handle_publish(self, client_socket, command):
        file_name = command.split()[1]
        with open(file_name, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"File {file_name} has been received and saved.")

        client_ip = client_socket.getpeername()[0]

        print(f"File '{file_name}' published from client {client_ip}")


        server_data_file_path = os.path.join(self.server_repo_path, 'Server_Data.txt')
        with open(server_data_file_path, 'a') as server_data_file:
            server_data_file.write(f"{file_name} - {client_ip}\n")

    def accept_connections(self):
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"Connection from {address} has been established.")
                self.clients_info[address] = client_socket
                self.clients[address] = []
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
                client_handler.start()
            except OSError:
                break

    def handle_client(self, client_socket, address):
        while True:
            try:
                command = client_socket.recv(1024).decode('utf-8')
                if not command:
                    break

                if command.startswith("publish"):
                    self.handle_publish(client_socket, command)
                elif command.startswith("fetch"):
                    self.handle_fetch(client_socket, command)
                elif command.startswith("delete"):
                    self.handle_delete(client_socket, command)
                elif command.startswith("upload"):
                    self.handle_upload(client_socket, command)
                else:
                    print(f"Unknown command from {address}: {command}")

            except ConnectionResetError:
                break
            except Exception as e:
                print(f"An error occurred with client {address}: {e}")
                break

        client_socket.close()
        del self.clients[address]
        print(f"Connection with {address} closed.")


    def handle_fetch(self, client_socket, command):
        file_name = command.split()[1]
        try:
            with open(file_name, 'rb') as file:
                data = file.read(1024)
                while data:
                    client_socket.send(data)
                    data = file.read(1024)
            print(f"File {file_name} has been sent.")
        except FileNotFoundError:
            print(f"File {file_name} not found.")

    def handle_delete(self, client_socket, command):
        file_name = command.split()[1]
        if os.path.exists(file_name):
            os.remove(file_name)
            client_socket.send(f"File {file_name} deleted.".encode('utf-8'))
        else:
            client_socket.send(f"File {file_name} not found.".encode('utf-8'))

    def handle_upload(self, client_socket, command):
        self.handle_publish(client_socket, command)

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

    def do_exit(self, arg):
        """Exit the server CLI"""
        self.server.shutdown_server()
        print("Shutting down the server.")
        return True

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

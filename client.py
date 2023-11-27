import socket
import threading
import cmd
import os

hardcoded_accounts = {
    "": "",
    "client2": "admin"
}


class FileClient:
    def __init__(self, host='localhost', port=5000):
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        self.client_socket.connect(self.server_address)
        print(f"Connected to server at {self.server_address}")

    def get_file_list(self, repo_path):
        try:
            # Lấy danh sách các file trong thư mục chỉ định
            files = [f for f in os.listdir(repo_path) if os.path.isfile(os.path.join(repo_path, f))]
            return files
        except FileNotFoundError:
            print(f"Repository path '{repo_path}' not found.")
            return []

    def handle_server_responses(self):
        while True:
            try:
                response = self.server_socket.recv(1024).decode('utf-8')
                if response:
                    print(f"Received response from server: {response}")  # Thêm dòng in này để kiểm tra phản hồi từ server
                    if response.startswith("Connected Clients:"):
                        # Xử lý danh sách client
                        connected_clients = response.split(":")[1].strip()
                        self.update_gui_client_list(connected_clients.split(', '))
                    else:
                        # Xử lý các phản hồi khác từ server
                        pass
            except:
                print("Server connection lost.")
                break

    def publish_file(self, local_path, file_name):
        self.send_command(f"publish {file_name}")
        try:
            with open(local_path, 'rb') as file:
                data = file.read(1024)
                while data:
                    self.client_socket.send(data)
                    data = file.read(1024)
            print(f"File {file_name} has been sent to the server.")
        except FileNotFoundError:
            print(f"File {local_path} not found.")

    def fetch_file(self, file_name):
        self.send_command(f"fetch {file_name}")
        with open(file_name, 'wb') as file:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"File {file_name} has been received from the server.")

    def delete_file(self, file_name):
        self.send_command(f"delete {file_name}")
        response = self.client_socket.recv(1024).decode('utf-8')
        print(response)

    def upload_file(self, local_path, file_name):
        # Tương tự như publish_file
        self.publish_file(local_path, file_name)
    
    def send_command(self, command):
        self.client_socket.send(command.encode('utf-8'))


    def close_connection(self):
        self.client_socket.close()

# Định nghĩa lớp ClientCLI để tương tác với server qua command line
class ClientCLI(cmd.Cmd):
    prompt = "> "

    def __init__(self, client):
        super().__init__()
        self.client = client

    def do_publish(self, arg):
        """Publish a file to the server"""
        self.client.publish_file(arg)

    def do_fetch(self, arg):
        """Fetch a file from the server"""
        self.client.fetch_file(arg)

    def do_delete(self, arg):
        """Delete a file from the server"""
        self.client.delete_file(arg)

    def do_upload(self, arg):
        """Upload a file to the server"""
        self.client.upload_file(arg)

if __name__ == "__main__":
    client = FileClient()
    client.connect_to_server()

    cli = ClientCLI(client)
    cli.cmdloop()

from client import FileClient
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import font
import os
import subprocess
import sys

hardcoded_accounts = {
        "": "",
        "client2": "admin"
    }

class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Client Login")
        self.client = FileClient()


        # Nhãn "Login" ở trên cùng
        self.login_label = tk.Label(master, text="Login", font=("Arial", 20))
        self.login_label.pack(pady=10)

        # Frame cho tên người dùng
        self.frame_username = tk.Frame(master)
        self.frame_username.pack(pady=5, padx=10, ipadx=5, ipady=5)
        self.label_username = tk.Label(self.frame_username, text="Username", font=("Arial", 11))
        self.label_username.pack(side=tk.LEFT, padx=5)
        self.entry_username = tk.Entry(self.frame_username, font=("Arial", 11))
        self.entry_username.pack(side=tk.LEFT, padx=5)

        # Frame cho mật khẩu
        self.frame_password = tk.Frame(master)
        self.frame_password.pack(pady=5, padx=10, ipadx=5, ipady=5)
        self.label_password = tk.Label(self.frame_password, text="Password", font=("Arial", 11))
        self.label_password.pack(side=tk.LEFT, padx=5)
        self.entry_password = tk.Entry(self.frame_password, show="*", font=("Arial", 11))
        self.entry_password.pack(side=tk.LEFT, padx=5)

        # Nút đăng nhập
        self.logbtn = tk.Button(master, text="Login", command=self._login_btn_clicked, font=("Arial", 11))
        self.logbtn.pack(ipadx=20, ipady=5, pady=(20, 30))

        # Nhãn "Don't have account? Register here"
        self.register_label = tk.Label(master, text="Don't have account? Register here", fg="blue", cursor="hand2")
        self.register_label.pack()
        self.register_label.bind("<Button-1>", self._register_label_clicked)


    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if hardcoded_accounts.get(username) == password:
            self._login_success()
        else:
            messagebox.showerror("Login error", "Incorrect username or password")

    def _register_label_clicked(self, event):
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.geometry("400x300")

    def _login_success(self):
        self.master.destroy()
        main_screen = tk.Tk()
        main_screen.geometry("1000x700")
        app = ClientMainScreen(main_screen)
        main_screen.mainloop()

class ClientMainScreen:
    def __init__(self, master):
        self.master = master
        master.title("CLIENT SIDE")
        self.client = FileClient()

        # Tạo sidebar
        self.setup_sidebar()

        # Tạo content wrapper
        self.setup_content_wrapper()

    def setup_sidebar(self):
        sidebar = tk.Frame(self.master, bg="gray", width=200)
        sidebar.pack(side="left", fill="y", expand=False)

        label = tk.Label(sidebar, text="CLIENT SIDE", bg="lightblue", fg="black", font=("Arial", 20), relief="ridge", borderwidth=2)
        label.pack(pady=20, padx=16)

        connect_btn = tk.Button(sidebar, text="Connect to server", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1, command=self.connect_to_server)
        quit_btn = tk.Button(sidebar, text="QUIT", bg="red", fg="white", width=12, font=("Arial", 11), height=1, command=self.quit_application)
        connect_btn.pack(side="bottom", pady=(10, 40), padx=2, ipady=8, ipadx=10)
        quit_btn.pack(side="bottom", pady=(10, 60), padx=2, ipady=4)

    def setup_content_wrapper(self):
        content_wrapper = tk.Frame(self.master, bg="lightgray")
        content_wrapper.pack(side="right", fill="both", expand=True)

        client_list_label = tk.Label(content_wrapper, text="Client Repository", font=("Arial", 16), bg="lightgray")
        client_list_label.pack(side="top", pady=5)

        # Phần hiển thị repository
        self.setup_repo_frame(content_wrapper)

        # Phần các nút bấm
        self.setup_file_management(content_wrapper)

        # Phần CLI
        self.setup_cli(content_wrapper)

    def setup_repo_frame(self, parent):
        repo_frame = tk.Frame(parent, bg="lightyellow")
        repo_frame.pack(side="top", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(repo_frame)
        scrollbar.pack(side="right", fill="y")

        custom_font = font.Font(family="Helvetica", size=12)
        self.repo_list = tk.Listbox(repo_frame, height=20, font=custom_font, yscrollcommand=scrollbar.set)
        self.repo_list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.repo_list.yview)

        self.repo_list.bind('<<ListboxSelect>>', self.on_file_select)
        self.update_repo_list()
    
    def update_repo_list(self):
        repo_path = "D:/Mang_MT/BTL/Client-Repo"
        files = os.listdir(repo_path)
        self.repo_list.delete(0, tk.END)
        for file in files:
            self.repo_list.insert(tk.END, file)

    def setup_file_management(self, parent):
        upfile_frame = tk.Frame(parent, bg="lightblue")
        upfile_frame.pack(side="top", fill="x", expand=False)

        upload_btn = tk.Button(upfile_frame, text="Upload File", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1, command=self.upload_file)
        delete_btn = tk.Button(upfile_frame, text="Delete File", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1, command=self.delete_file)
        # upload_to_server_btn = tk.Button(upfile_frame, text="Upload To Server", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1, command=self.upload_to_server)

        upload_btn.grid(row=0, column=0, padx=(200, 50), pady=20)
        delete_btn.grid(row=0, column=1, padx=(50,200), pady=20)
        # upload_to_server_btn.grid(row=0, column=2, padx=(50, 110), pady=20)

    def setup_cli(self, parent):
        cli = tk.Frame(parent, bg="lightgray", height=50)
        cli.pack(side="top", fill="x", expand=False, pady=(10,10))

        self.cli_input = tk.Entry(cli, bd=3, font=("Arial", 13))
        self.cli_input.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        enter_button = tk.Button(cli, text="Enter", font=("Arial", 13), height=1, command=self.execute_cli_command)
        enter_button.pack(side="left", padx=10, pady=10, ipadx=20)

    # Định nghĩa các phương thức cho các nút
    def connect_to_server(self):
        self.client.connect_to_server()

    def upload_file(self):
        # Phương thức tải lên file
        filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        if filename:
            self.client.publish_file(filename)
        self.update_repo_list()

    def delete_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file to delete")
        if filename:
            self.client.delete_file(filename)
            messagebox.showinfo("Delete File", f"Deleted file: {filename}")
        self.update_repo_list()

    # def upload_to_server(self):
    #     filename = filedialog.askopenfilename(initialdir="/", title="Select file to upload")
    #     if filename:
    #         # Giả sử FileClient có phương thức upload_to_server
    #         self.client.upload_to_server(filename)
    #         messagebox.showinfo("Upload to Server", f"Uploaded file to server: {filename}")

    def upload_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file to upload")
        if filename:
            self.client.publish_file(filename)
            messagebox.showinfo("Upload to Server", f"Uploaded file to server: {filename}")
    
    def on_file_select(self, event):
        index = self.repo_list.curselection()

        if index:
            file_name = self.repo_list.get(index[0])
            full_path = os.path.join(r'D:\Mang_MT\BTL\Client-Repo', file_name)

            try:
                if sys.platform == "win32":
                    os.startfile(full_path)
                elif sys.platform == "darwin":  # macOS
                    subprocess.run(["open", full_path])
                else:  # Linux và các hệ điều hành khác
                    subprocess.run(["xdg-open", full_path])
            except Exception as e:
                print(f"Không thể mở file: {file_name}. Lỗi: {e}")
        else:
            print("No file selected !!")

    
    def display_file_content(self, content):
        top = tk.Toplevel(self)
        text_widget = tk.Text(top)
        text_widget.insert(tk.END, content)
        text_widget.pack(expand=True, fill='both')

    

    def execute_cli_command(self):
        # Phương thức xử lý lệnh từ CLI
        command = self.cli_input.get()
        args = command.split()

        if len(args) == 0:
            messagebox.showerror("Error", "No command entered")
            return

        if args[0] == "publish":
            if len(args) < 2:
                messagebox.showerror("Error", "No file specified for publish")
            else:
                local_path = args[1]  # Đây là đường dẫn cục bộ của tệp
                file_name = os.path.basename(local_path)  # Lấy tên tệp từ đường dẫn cục bộ
                self.client.publish_file(local_path, file_name)  # Truyền cả đường dẫn và tên tệp
                messagebox.showinfo("Publish File", f"Published file: {file_name}")

        elif args[0] == "fetch":
            if len(args) < 2:
                messagebox.showerror("Error", "No file specified for fetch")
            else:
                filename = args[1]
                self.client.fetch_file(filename)
                messagebox.showinfo("Fetch File", f"Fetched file: {filename}")

        elif args[0] == "exit":
            self.quit_application()

        else:
            messagebox.showerror("Error", f"Unknown command: {args[0]}")

        self.cli_input.delete(0, tk.END)


    def quit_application(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = ClientGUI(root)
    root.mainloop()

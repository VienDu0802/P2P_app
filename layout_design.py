import tkinter as tk
from tkinter import messagebox

class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Client Login")

        # Nhãn "Login" ở trên cùng
        self.login_label = tk.Label(master, text="Login", font=("Arial", 20))
        self.login_label.pack(pady=10)

        # Frame cho tên người dùng
        self.frame_username = tk.Frame(master)
        self.frame_username.pack(pady=5, padx=10, ipadx=5, ipady=5)
        self.label_username = tk.Label(self.frame_username, text="Username", font=("Arial", 11))
        self.label_username.pack(side=tk.LEFT, padx=5)
        self.entry_username = tk.Entry(self.frame_username,font=("Arial", 11))
        self.entry_username.pack(side=tk.LEFT, padx=5)

        # Frame cho mật khẩu
        self.frame_password = tk.Frame(master)
        self.frame_password.pack(pady=5, padx=10, ipadx=5, ipady=5)
        self.label_password = tk.Label(self.frame_password, text="Password",font=("Arial", 11))
        self.label_password.pack(side=tk.LEFT, padx=5)
        self.entry_password = tk.Entry(self.frame_password, show="*",font=("Arial", 11))
        self.entry_password.pack(side=tk.LEFT, padx=5)

        # Nút đăng nhập
        self.logbtn = tk.Button(master, text="Login", command=self._login_btn_clicked, font=("Arial", 11))
        self.logbtn.pack(ipadx=20, ipady=5 ,pady=(20,30))

        # Nhãn "Don't have account? Register here"
        self.register_label = tk.Label(master, text="Don't have account? Register here", fg="blue", cursor="hand2")
        self.register_label.pack()
        self.register_label.bind("<Button-1>", self._register_label_clicked)

    def _login_btn_clicked(self):
        # Xử lý đăng nhập
        username = self.entry_username.get()
        password = self.entry_password.get()
        # Thay thế logic đăng nhập thực tế ở đây
        if username == "" and password == "":
            self._login_success()
        else:
            messagebox.showerror("Login error", "Incorrect username or password")

    def _register_label_clicked(self, event):
        # Mở cửa sổ đăng ký
        self.register_window = tk.Toplevel(self.master)
        self.register_window.title("Register")
        self.register_window.geometry("400x300")

        # Nhãn "Register" ở trên cùng
        register_label = tk.Label(self.register_window, text="Register", font=("Arial", 18))
        register_label.pack(pady=16)

        # Frame chính cho nhập liệu
        input_frame = tk.Frame(self.register_window)
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        # Tạo nhãn và trường nhập liệu
        labels = ["Username", "Password", "Confirm Password"]
        entries = []
        for i, text in enumerate(labels):
            label = tk.Label(input_frame, text=text, font=("Arial", 11))
            label.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            entry = tk.Entry(input_frame, font=("Arial", 11))
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=5)
            entries.append(entry)

        # Nút đăng ký
        register_btn = tk.Button(self.register_window, text="Register",font=("Arial", 12),
             command=lambda: self._register_btn_clicked(entries[0].get(), entries[1].get(), entries[2].get()))
        register_btn.pack(pady=(20,10), ipadx=10, ipady= 4)

    def _register_btn_clicked(self, username, password, confirm_password):
        # Xử lý đăng ký
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return
        # Thêm logic đăng ký tài khoản ở đây
        messagebox.showinfo("Success", "Registration successful")
        self.register_window.destroy()

    def _login_success(self):
        # Đóng màn hình đăng nhập và mở màn hình chính
        self.master.destroy()
        main_screen = tk.Tk()
        main_screen.geometry("1000x700")
        app = ClientMainScreen(main_screen)
        main_screen.mainloop()


class ClientMainScreen:
    def __init__(self, master):
        self.master = master
        master.title("CLIENT SIDE")
    
        # Sidebar
        sidebar = tk.Frame(master, bg="gray", width=200)
        sidebar.pack(side="left", fill="y", expand=False)
    
        # Tạo nhãn "CLIENT SIDE"
        label = tk.Label(sidebar, text="CLIENT SIDE", bg="lightblue", fg="black", font=("Arial", 20), relief="ridge", borderwidth=2)
        label.pack(pady=20, padx=16)
    
        # Tạo các nút bấm
        button2 = tk.Button(sidebar, text="Connect to server", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1)
        button3 = tk.Button(sidebar, text="QUIT", bg="red", fg="white", width=12, font=("Arial", 11), height=1)
        button3.pack(side="bottom", pady=(10, 60), padx=2, ipady=4)
        button2.pack(side="bottom", pady=(10, 40), padx=2, ipady=8, ipadx=10)
        
        # Content Wrapper
        content_Wrapper = tk.Frame(master, bg="lightgray")
        content_Wrapper.pack(side="right", fill="both", expand=True)
        
        # Nhãn "Client List"
        client_list_label = tk.Label(content_Wrapper, text="Client Repository", font=("Arial", 16), bg="lightgray")
        client_list_label.pack(side="top", pady=5)
    
        # Content
        content = tk.Frame(content_Wrapper, bg="white")
        content.pack(side="top", fill="both", expand=True)

        # repo
        repo_frame = tk.Frame(content,bg="lightgray")
        repo_frame.pack(side="top",fill="both", expand=True)

        #up file
        upfile_frame = tk.Frame(content, bg="lightgreen")
        upfile_frame.pack(side="bottom", fill="both", expand=False)
        
        Upfile_Btn = tk.Button(upfile_frame, text="Upload File", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1)
        Upfile_Btn.grid(row=0, column=0, padx=(110,50), pady=20)
        
        Delete_Btn = tk.Button(upfile_frame, text="Delete File", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1)
        Delete_Btn.grid(row=0, column=1, padx=30, pady=20)
        
        UploadToServer = tk.Button(upfile_frame, text="Upload To Server", bg="lightgray", fg="black", font=("Arial", 11), width=12, height=1)
        UploadToServer.grid(row=0, column=2, padx=(50,110), pady=20)

        # CLI
        cli = tk.Frame(content_Wrapper, bg="lightgray", height=50)
        cli.pack(side="bottom", fill="x", expand=False, padx=50, pady=10)
    
        cli_input = tk.Entry(cli, bd=3, font=("Arial", 13))
        cli_input.pack(side="left", fill="x", expand=True, padx=10, pady=10)
    
        enter_button = tk.Button(cli, text="Enter", font=("Arial", 13), height=1)
        enter_button.pack(side="left", padx=10, pady=10, ipadx=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")  # Kích thước cho màn hình đăng nhập
    app = ClientGUI(root)
    root.mainloop()

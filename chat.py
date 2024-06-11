import tkinter as tk
from tkinter import scrolledtext
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from encryption import encrypt_message, decrypt_message

# Global constants for connection
HOST = '127.0.0.1'  # Localhost for testing, use the actual IP address in real scenarios
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

# GUI setup
class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Encrypted Chat")

        self.chat_box = scrolledtext.ScrolledText(master)
        self.chat_box.pack(padx=20, pady=5)
        self.chat_box.config(state=tk.DISABLED)

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack(padx=20, pady=5)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=20, pady=5)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)

        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        encrypted_message = encrypt_message(message)
        self.client_socket.send(encrypted_message)
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, "You: " + message + "\n")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.yview(tk.END)

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client_socket.recv(BUFSIZ)
                message = decrypt_message(encrypted_message)
                self.chat_box.config(state=tk.NORMAL)
                self.chat_box.insert(tk.END, "Them: " + message + "\n")
                self.chat_box.config(state=tk.DISABLED)
                self.chat_box.yview(tk.END)
            except OSError:
                break

def start_client():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_client()

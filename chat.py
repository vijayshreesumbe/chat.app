import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
from threading import Thread

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Application")
        self.master.geometry("400x400")
        self.create_widgets()
        self.setup_networking()

    def create_widgets(self):
        self.chat_box = scrolledtext.ScrolledText(self.master, height=15, width=40, bg='lightgray')
        self.chat_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.message_entry = tk.Entry(self.master, width=30)
        self.message_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message, bg='lightblue')
        self.send_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        # Configure grid weights to make chat box expandable
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def setup_networking(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('localhost', 5555))  # Change IP address and port accordingly
        except ConnectionRefusedError:
            messagebox.showerror("Error", "Could not connect to the server. Please make sure the server is running.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
            self.master.destroy()

        # Start a new thread to receive messages from the server
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            self.chat_box.insert(tk.END, f"You: {message}\n", 'you')
            self.message_entry.delete(0, tk.END)
            self.client_socket.send(message.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_box.insert(tk.END, f"Friend: {message}\n", 'friend')
                self.chat_box.see(tk.END)
            except ConnectionAbortedError:
                break

def main():
    root = tk.Tk()
    app = ChatApp(root)

    # Configure tags for message styling
    app.chat_box.tag_config('you', justify='right')
    app.chat_box.tag_config('friend', justify='left')

    root.mainloop()

if __name__ == "__main__":
    main()

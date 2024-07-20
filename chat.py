import os
import ssl
import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from OpenSSL import crypto

# Paths for SSL certificates and keys
CERT_DIR = "certs"
SERVER_CERT = os.path.join(CERT_DIR, "server.crt")
SERVER_KEY = os.path.join(CERT_DIR, "server.key")
CLIENT_CERT = os.path.join(CERT_DIR, "client.crt")
CLIENT_KEY = os.path.join(CERT_DIR, "client.key")

def generate_certificates():
    if not os.path.exists(CERT_DIR):
        os.makedirs(CERT_DIR)

    # Generate server certificate and key
    if not os.path.exists(SERVER_CERT) or not os.path.exists(SERVER_KEY):
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        cert = crypto.X509()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365*24*60*60)
        cert.set_subject(crypto.X509Name(dict(CN="server")))
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(key, 'sha256')

        with open(SERVER_KEY, "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        with open(SERVER_CERT, "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    # Generate client certificate and key
    if not os.path.exists(CLIENT_CERT) or not os.path.exists(CLIENT_KEY):
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        cert = crypto.X509()
        cert.set_serial_number(1001)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365*24*60*60)
        cert.set_subject(crypto.X509Name(dict(CN="client")))
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(key, 'sha256')

        with open(CLIENT_KEY, "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        with open(CLIENT_CERT, "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    server_socket = ssl.wrap_socket(server_socket, server_side=True, certfile=SERVER_CERT, keyfile=SERVER_KEY)

    clients = []

    def handle_client(client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    broadcast(message, client_socket)
                else:
                    break
            except ConnectionResetError:
                break
        client_socket.close()
        clients.remove(client_socket)

    def broadcast(message, source_socket):
        for client in clients:
            if client != source_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    pass

    print("Server listening on port 12345")
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

def start_client():
    class ChatClient:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.sock = None
            self.root = tk.Tk()
            self.root.title("Chat Client")
            self.create_gui()

        def create_gui(self):
            self.chat_display = tk.Text(self.root, state='disabled', width=50, height=15)
            self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            self.chat_message = ttk.Entry(self.root, width=50)
            self.chat_message.grid(row=1, column=0, padx=10, pady=10)

            ttk.Button(self.root, text="Send", command=self.send_message).grid(row=1, column=1, padx=10, pady=10)
            ttk.Button(self.root, text="Connect", command=self.connect).grid(row=2, column=0, padx=10, pady=10)
            ttk.Button(self.root, text="Disconnect", command=self.disconnect).grid(row=2, column=1, padx=10, pady=10)

        def connect(self):
            if self.sock is not None:
                messagebox.showwarning("Warning", "Already connected.")
                return

            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
            self.sock = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=self.host)
            self.sock.connect((self.host, self.port))

            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()

        def disconnect(self):
            if self.sock is None:
                messagebox.showwarning("Warning", "Not connected.")
                return

            self.sock.close()
            self.sock = None

        def send_message(self):
            message = self.chat_message.get()
            if not message:
                messagebox.showwarning("Warning", "Message cannot be empty.")
                return

            if self.sock:
                self.sock.send(message.encode('utf-8'))
                self.chat_message.delete(0, 'end')
                self.chat_display.config(state='normal')
                self.chat_display.insert('end', f"You: {message}\n")
                self.chat_display.config(state='disabled')

        def receive_messages(self):
            while True:
                try:
                    message = self.sock.recv(1024).decode('utf-8')
                    if message:
                        self.chat_display.config(state='normal')
                        self.chat_display.insert('end', f"Friend: {message}\n")
                        self.chat_display.config(state='disabled')
                    else:
                        break
                except:
                    break

        def run(self):
            self.root.mainloop()

    client = ChatClient('127.0.0.1', 12345)
    client.run()

if __name__ == "__main__":
    generate_certificates()
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    client_thread = threading.Thread(target=start_client)
    client_thread.start()

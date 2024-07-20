import tkinter as tk
from tkinter import ttk, messagebox
import threading

class StressTesterGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Stress Tester")
        self.geometry("600x400")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill='both')

        self.create_layer4_tab()
        self.create_layer7_tab()
        self.create_xmlrpc_tab()
        self.create_chat_tab()

    def create_layer4_tab(self):
        self.layer4_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.layer4_frame, text='Layer 4 Attack')

        ttk.Label(self.layer4_frame, text="Target IP:").grid(row=0, column=0, padx=10, pady=10)
        self.layer4_ip = ttk.Entry(self.layer4_frame)
        self.layer4_ip.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.layer4_frame, text="Target Port:").grid(row=1, column=0, padx=10, pady=10)
        self.layer4_port = ttk.Entry(self.layer4_frame)
        self.layer4_port.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.layer4_frame, text="Protocol:").grid(row=2, column=0, padx=10, pady=10)
        self.layer4_protocol = ttk.Combobox(self.layer4_frame, values=["TCP", "UDP"])
        self.layer4_protocol.grid(row=2, column=1, padx=10, pady=10)

        self.layer4_start_button = ttk.Button(self.layer4_frame, text="Start", command=self.start_layer4_attack)
        self.layer4_start_button.grid(row=3, column=0, padx=10, pady=10)

        self.layer4_stop_button = ttk.Button(self.layer4_frame, text="Stop", command=self.stop_layer4_attack)
        self.layer4_stop_button.grid(row=3, column=1, padx=10, pady=10)

    def create_layer7_tab(self):
        self.layer7_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.layer7_frame, text='Layer 7 Attack')

        ttk.Label(self.layer7_frame, text="Target URL:").grid(row=0, column=0, padx=10, pady=10)
        self.layer7_url = ttk.Entry(self.layer7_frame)
        self.layer7_url.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.layer7_frame, text="DOS Type:").grid(row=1, column=0, padx=10, pady=10)
        self.layer7_dos_type = ttk.Combobox(self.layer7_frame, values=["GET", "POST"])
        self.layer7_dos_type.grid(row=1, column=1, padx=10, pady=10)

        self.layer7_start_button = ttk.Button(self.layer7_frame, text="Start", command=self.start_layer7_attack)
        self.layer7_start_button.grid(row=2, column=0, padx=10, pady=10)

        self.layer7_stop_button = ttk.Button(self.layer7_frame, text="Stop", command=self.stop_layer7_attack)
        self.layer7_stop_button.grid(row=2, column=1, padx=10, pady=10)

    def create_xmlrpc_tab(self):
        self.xmlrpc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.xmlrpc_frame, text='XML-RPC Attack')

        ttk.Label(self.xmlrpc_frame, text="URL:").grid(row=0, column=0, padx=10, pady=10)
        self.xmlrpc_url = ttk.Entry(self.xmlrpc_frame)
        self.xmlrpc_url.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.xmlrpc_frame, text="Method Name:").grid(row=1, column=0, padx=10, pady=10)
        self.xmlrpc_method = ttk.Entry(self.xmlrpc_frame)
        self.xmlrpc_method.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.xmlrpc_frame, text="Parameters:").grid(row=2, column=0, padx=10, pady=10)
        self.xmlrpc_params = ttk.Entry(self.xmlrpc_frame)
        self.xmlrpc_params.grid(row=2, column=1, padx=10, pady=10)

        self.xmlrpc_start_button = ttk.Button(self.xmlrpc_frame, text="Start", command=self.start_xmlrpc_attack)
        self.xmlrpc_start_button.grid(row=3, column=0, padx=10, pady=10)

        self.xmlrpc_stop_button = ttk.Button(self.xmlrpc_frame, text="Stop", command=self.stop_xmlrpc_attack)
        self.xmlrpc_stop_button.grid(row=3, column=1, padx=10, pady=10)

    def create_chat_tab(self):
        self.chat_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.chat_frame, text='Chat Client')

        self.chat_display = tk.Text(self.chat_frame, state='disabled', width=50, height=15)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.chat_message = ttk.Entry(self.chat_frame, width=50)
        self.chat_message.grid(row=1, column=0, padx=10, pady=10)

        self.chat_send_button = ttk.Button(self.chat_frame, text="Send", command=self.send_chat_message)
        self.chat_send_button.grid(row=1, column=1, padx=10, pady=10)

        self.chat_connect_button = ttk.Button(self.chat_frame, text="Connect", command=self.connect_chat)
        self.chat_connect_button.grid(row=2, column=0, padx=10, pady=10)

        self.chat_disconnect_button = ttk.Button(self.chat_frame, text="Disconnect", command=self.disconnect_chat)
        self.chat_disconnect_button.grid(row=2, column=1, padx=10, pady=10)

    def start_layer4_attack(self):
        target_ip = self.layer4_ip.get()
        target_port = int(self.layer4_port.get())
        protocol = self.layer4_protocol.get()
        if target_ip and target_port and protocol:
            self.layer4_thread = threading.Thread(target=launch_stress_test, args=(None, None, target_ip, target_port, protocol))
            self.layer4_thread.start()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def stop_layer4_attack(self):
        if hasattr(self, 'layer4_thread'):
            self.layer4_thread.kill_received = True
            self.layer4_thread.join()

    def start_layer7_attack(self):
        site = self.layer7_url.get()
        dos_type = self.layer7_dos_type.get()
        if site and dos_type:
            self.layer7_thread = threading.Thread(target=launch_stress_test, args=(site, dos_type, None, None, None))
            self.layer7_thread.start()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def stop_layer7_attack(self):
        if hasattr(self, 'layer7_thread'):
            self.layer7_thread.kill_received = True
            self.layer7_thread.join()

    def start_xmlrpc_attack(self):
        site = self.xmlrpc_url.get()
        method_name = self.xmlrpc_method.get()
        params = self.xmlrpc_params.get().split()
        if site and method_name:
            self.xmlrpc_thread = threading.Thread(target=launch_stress_test, args=(site, method_name, params))
            self.xmlrpc_thread.start()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def stop_xmlrpc_attack(self):
        if hasattr(self, 'xmlrpc_thread'):
            self.xmlrpc_thread.kill_received = True
            self.xmlrpc_thread.join()

    def connect_chat(self):
        self.chat_thread = threading.Thread(target=chat_client)
        self.chat_thread.start()

    def disconnect_chat(self):
        if hasattr(self, 'chat_thread'):
            self.chat_thread.kill_received = True
            self.chat_thread.join()

    def send_chat_message(self):
        message = self.chat_message.get()
        # Implement the send message logic here
        self.chat_message.delete(0, 'end')
        self.chat_display.config(state='normal')
        self.chat_display.insert('end', f"You: {message}\n")
        self.chat_display.config(state='disabled')

if __name__ == "__main__":
    app = StressTesterGUI()
    app.mainloop()

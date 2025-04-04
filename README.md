#server
import socket
import threading

# List to store clients
clients = []

# Handle communication with each client
def handle_client(client_socket, client_address):
    print(f"New connection: {client_address}")
    
    while True:
        try:
            # Receive a message from the client
            message = client_socket.recv(1024).decode('utf-8')
            
            if message:
                print(f"Received from {client_address}: {message}")
                # Broadcast message to all clients
                broadcast(message, client_socket)
            else:
                # Connection closed
                remove_client(client_socket)
                break
        except:
            continue

# Broadcast the message to all clients except the sender
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                continue

# Remove client from the list of clients
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

# Start the server
def start_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server running on {host}:{port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()

#client 
import socket
import tkinter as tk
from tkinter import scrolledtext
import threading

# Connect to the server
def connect_to_server(host='127.0.0.1', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

# Send message to the server
def send_message():
    message = message_entry.get()
    client_socket.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)

# Receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, f"Server: {message}\n")
            chat_box.config(state=tk.DISABLED)
        except:
            break

# Create the GUI
def create_gui():
    global chat_box, message_entry, client_socket
    
    window = tk.Tk()
    window.title("Chat Client")

    chat_box = scrolledtext.ScrolledText(window, width=50, height=20, state=tk.DISABLED)
    chat_box.grid(row=0, column=0, padx=10, pady=10)

    message_entry = tk.Entry(window, width=40)
    message_entry.grid(row=1, column=0, padx=10, pady=10)

    send_button = tk.Button(window, text="Send", width=20, command=send_message)
    send_button.grid(row=1, column=1, padx=10, pady=10)

    window.protocol("WM_DELETE_WINDOW", window.quit)
    window.mainloop()

if __name__ == "__main__":
    client_socket = connect_to_server()
    threading.Thread(target=receive_messages, daemon=True).start()
    create_gui()


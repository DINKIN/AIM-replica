import socket
import select
import errno
import tkinter as tk

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

my_username = 'Client'

root = tk.Tk()
top = tk.Canvas(root, height=100, width=100)
top.pack()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)


def send_message_to_server(event=None):
    message = msg.get()
    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message)

    username_header = client_socket.recv(HEADER_LENGTH)
    username_length = int(username_header.decode('utf-8').strip())
    username = client_socket.recv(username_length).decode('utf-8')

    message_header = client_socket.recv(HEADER_LENGTH)
    message_length = int(message_header.decode('utf-8').strip())
    message = client_socket.recv(message_length).decode('utf-8')
    print(f'{username} --- {message}')


msg = tk.StringVar()
T2 = tk.Entry(top, textvariable=msg)
T2.bind('<Return>', send_message_to_server)
T2.pack()

root.mainloop()
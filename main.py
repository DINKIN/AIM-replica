import tkinter as tk
from tkinter import ttk
from tkinter import *
import PIL
from PIL import ImageTk, Image
import socket
import select

WIN_HEIGHT = 500
WIN_WIDTH = 300

GRAY = '#dbdace'
BLUE = '#2565a8'
LIGHTBLUE = '#adc7db'

root = tk.Tk()
root.title('AOL Instant Messenger')
root.resizable(width = False, height = False) 

def open_server(event):
    failed_count = 0
    my_username = username_entry.get()
    password = password_entry.get()


    def send_message_to_server(event=None):
        message = msg.get()
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
        user_chat_info = T2.get()

        msg.set('')
        T.insert(tk.END, my_username + ': ')
        T.insert(tk.END, user_chat_info)
        T.insert(tk.END, '\n' )

    if password:
        HEADER_LENGTH = 10
        IP = "127.0.0.1"
        PORT = 1234

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        client_socket.setblocking(False)
        username = my_username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)

        TOP_HEIGHT = 375
        TOP_WIDTH = 500
        top = Toplevel(root, height=TOP_HEIGHT, width=TOP_WIDTH, bg='#dbdace') 
        top.title('AOL System Msg. ' + my_username + ' - Message')

        msg = tk.StringVar()
        T2 = tk.Entry(top, textvariable=msg)
        T2.bind('<Return>', send_message_to_server)
        T2.place(relx=0.005, rely=0.55, relheight=0.2, relwidth=0.989)

        T = tk.Text(top)
        T.place(relx=0.05, rely=0.06, relheight=0.4, relwidth=0.9)
        T.configure(font=('Times New Roman', 13))

        send_button = tk.Button(top, text='Send')
        send_button.bind('<Button-1>', send_message_to_server)
        send_button.place(relx=0.85, rely=0.8, relheight=0.17, relwidth=0.145)

        top.mainloop()
        
    else:
        failed_label = tk.Label(canvas, text='Incorrect Password! Try agian...', font=('Helvetica', 7), bg=GRAY)
        failed_label.place(relx=0.07, rely=0.8, relheight=0.05, relwidth=0.5)
        failed_count = 1

image = Image.open("theguy.png")
basewidth = 130

canvas = tk.Canvas(root, height=WIN_HEIGHT, width=WIN_WIDTH, bg=GRAY)
canvas.pack()

canvas2 = tk.Canvas(root, height=200, width=WIN_WIDTH-30, bg=BLUE)
wpercent = (basewidth / float(image.size[0]))
hsize = int((float(image.size[1]) * float(wpercent)))
image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
item4 = canvas2.create_image(175, 90, image=photo)
canvas2.place(relx=0.05,rely=0.005,relheight=0.5,relwidth=0.9)


title_name = tk.Label(canvas2, text='AOL Instant Messenger', font=('Helvetica', 16), fg='white', bg=BLUE)
title_name.place(relx=0.03,rely=0.85,relheight=0.09,relwidth=0.9)

signon_button = tk.Button(canvas, text='Sign On')
signon_button.bind('<Button-1>', open_server)
signon_button.place(relx=0.7, rely=0.9, relheight=0.05, relwidth=0.2)

option = [''] # dropdown menu options
clicked = StringVar()
clicked.set(option[0])
drop = OptionMenu(canvas, clicked, *option)
drop.config(bg=LIGHTBLUE)
drop.place(relx=0.8, rely=0.6, relheight=0.05, relwidth=0.11)

username_entry = tk.Entry(canvas, bg='white')
username_entry.bind('<Return>', open_server)
username_entry.place(relx=0.095, rely=0.6, relheight=0.05, relwidth=0.7)

password = True
password_entry = tk.Entry(canvas, bg='white')
password_entry.bind('<Return>', open_server)
password_entry.place(relx=0.095, rely=0.75, relheight=0.05, relwidth=0.8)

username_label = tk.Label(canvas, text='ScreenName', font=('helvetica', 12, 'bold'), bg=GRAY, fg='#2a2e7a')
username_label.place(relx=0.09, rely=0.55)

password_label = tk.Label(canvas, text='Password', font=('helvetica', 10, 'bold'), bg=GRAY, fg='black')
password_label.place(relx=0.09, rely=0.7)


root.mainloop()

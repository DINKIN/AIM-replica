import tkinter as tk
from tkinter import ttk
from tkinter import * 
from tkinter import colorchooser
import PIL
from PIL import ImageTk, Image
import socket
import select
import errno
import threading
import time
from playsound import playsound
import json

WIN_HEIGHT = 500
WIN_WIDTH = 300
WIN2_HEIGHT = 300
WIN2_WIDTH = 500


GRAY = '#dbdace'
BLUE = '#2565a8'
LIGHTBLUE = '#adc7db'

root = tk.Tk()
root.title('AOL Instant Messenger')
root.resizable(width = False, height = False)


def usr_create(event):
    crt_usr_gui = Toplevel(root, height=WIN2_HEIGHT, width=WIN2_WIDTH, bg='white') 
    crt_usr_gui.title('Creat an Account!')

    def create_usr(event):
        uN = pick_username.get()
        pW = pick_password1.get()
        pW2 = pick_password2.get()

        if pW != pW2:
            print('Passwords dont match!')

        def login(usr):
            if uN in usr.keys():
                if pW == usr[uN]:
                    welcome_txt = "Account Already Exists for Screen Name: "
                    welcome_label = tk.Label(crt_usr_gui, text=welcome_txt + uN)
                    welcome_label.pack(side='bottom')
                else:
                    inc_pass = "Incorrect password."
                    inc_pass = tk.Label(crt_usr_gui, text=welcome_txt)
                    inc_pass.pack(side='bottom')
                    return False

            else:
                welcome_txt = "Account Created! You may not close this window "
                welcome_label = tk.Label(crt_usr_gui, text=welcome_txt + uN)
                welcome_label.pack(side='bottom')
                usr[uN] = pW

            writeUsers(usr)
            return True

        def readUsers():
            try:
                with open("users.json", "r") as f:
                    return json.load(f)
            except FileNotFoundError:
                return {}

        def writeUsers(usr):
            with open("users.json", "w+") as f:
                    json.dump(usr, f)

        users = readUsers()
        success = login(users)

        while not success:
            success = login(users)
            break

    crt_canvas = tk.Canvas(crt_usr_gui, height=WIN2_HEIGHT, width=WIN2_WIDTH, bg='gray')
    crt_canvas.pack()

    usrname = tk.StringVar()
    pick_username = tk.Entry(crt_usr_gui, textvariable=usrname, bg='white')
    pick_username.bind('<Return>', create_usr)
    pick_username.place(relx=0.095, rely=0.3, relheight=0.08, relwidth=0.8)

    pick_password1 = tk.Entry(crt_usr_gui, bg='white')
    pick_password1.bind('<Return>', create_usr)
    pick_password1.config(show="*")                 # makes it do the ****** for passwords
    pick_password1.place(relx=0.095, rely=0.5, relheight=0.08, relwidth=0.8)

    pick_password2 = tk.Entry(crt_usr_gui, bg='white')
    pick_password2.bind('<Return>', create_usr)
    pick_password2.config(show="*")                 # makes it do the ****** for passwords
    pick_password2.place(relx=0.095, rely=0.6, relheight=0.08, relwidth=0.8)

    submit_button = tk.Button(crt_usr_gui, text='Submit')
    submit_button.bind('<Button-1>', create_usr)
    submit_button.place(relx=0.4, rely=0.8, relheight=0.08, relwidth=0.2)

    sign_up_label = tk.Label(crt_usr_gui, text='Sign Up!', font=('helvetica', 14, 'bold'), bg='gray', fg='black')
    sign_up_label.place(relx=0.4, rely=0.08)

    crt_usr_gui.mainloop()

def open_server(event):
    failed_count = 0
    my_username = username_entry.get()
    password = password_entry.get()


    def font_bar_action(event):   
        nonlocal my_txt_color_fg
        my_txt_color_fg = colorchooser.askcolor()[1]
        T.tag_config('messagecolor', background='white', foreground=my_txt_color_fg)


    def send_message_to_server(event):
        message = msg.get()
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
        user_chat_info = T2.get()
        msg.set('')
        playsound('sounds/receive.mp3')
        T.tag_config('sender', background="white", foreground="blue")
        T.tag_config('messagecolor', background='white', foreground=my_txt_color_fg)
        T.insert('end', my_username + ': ', 'sender') 
        T.insert('end', user_chat_info + '\n', 'messagecolor')
    
    
    def insert_incomming(incomming_message, incomming_username):
        playsound('sounds/send.mp3')
        T.tag_config('receiver', background="white", foreground="red")
        T.insert('end', incomming_username + ': ', 'receiver', incomming_message + '\n')  # Puts text in Top (T) then colors the username red for incomming messages \n for new line


    def bottom_bar_action(event):
        pass

    def donothing():   # currently set to Help dropdown menu
        pass

    def about_me():
        TOP_HEIGHT2 = 150
        TOP_WIDTH2 = 300
        top = Toplevel(root, height=TOP_HEIGHT2, width=TOP_WIDTH2, bg='white') 
        top.title('About')
        info_me = tk.Label(top, text='Project by Terrnova Technologies\nPlease report all bugs to\ninfo@terratechblog.com', font=('helvetica', 14), bg='white')
        info_me.pack()

        its_me = PhotoImage(file="pics/itsme.png")
        me_button = tk.Button(top, image = its_me)
        me_button.bind('<Button-1>', donothing)
        me_button.pack()

        top.mainloop()

    def check_incomming_msg():
        while True:
            try:
                while True:
                    username_header = client_socket.recv(HEADER_LENGTH)

                    if not len(username_header):
                        print('Connection closed by the server')
                        sys.exit()

                    username_length = int(username_header.decode('utf-8').strip())
                    incomming_username = client_socket.recv(username_length).decode('utf-8')

                    message_header = client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    incomming_message = client_socket.recv(message_length).decode('utf-8')

                    if incomming_message:
                        insert_incomming(incomming_message,incomming_username)
                        time.sleep(4)
                break

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                continue
                time.sleep(1)

            except Exception as e:
                print('Reading error: '.format(str(e)))
                sys.exit()
            break
            time.sleep(1)
        time.sleep(1)
    
    def readUsers():
        try:
            with open("users.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    usr = readUsers()
    if my_username in usr.keys():
        if password == usr[my_username]:
            HEADER_LENGTH = 10
            IP = "10.0.0.28"
            PORT = 1234

            my_txt_color_fg = ''    # This is a non local variable

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((IP, PORT))
            client_socket.setblocking(False)
            username = my_username.encode('utf-8')
            username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(username_header + username)

            thread1 = threading.Thread(target=check_incomming_msg)
            thread1.start()
            playsound('sounds/login1.mp3')

            TOP_HEIGHT = 375
            TOP_WIDTH = 505
            top = Toplevel(root, height=TOP_HEIGHT, width=TOP_WIDTH, bg='#dbdace') 
            top.title('AOL System Msg. ' + my_username + ' - Message')

            T = tk.Text(top)   # Top text box (I chose Text for recolor and scrollbar functions)
            T.place(relx=0.05, rely=0.06, relheight=0.4, relwidth=0.9)
            T.configure(font=('Times New Roman', 13))

            scrollbar = Scrollbar(T)
            scrollbar.pack(side=RIGHT, fill=Y)
            T.config(yscrollcommand=scrollbar.set)

            msg = tk.StringVar()   # Bottom text box (I chose entry for the bind feature to Enter Key)
            T2 = tk.Entry(top, textvariable=msg)
            T2.bind('<Return>', send_message_to_server)
            T2.place(relx=0.005, rely=0.55, relheight=0.2, relwidth=0.989)

            send_button_photo = PhotoImage(file="pics/sendbutton.png")
            send_button = tk.Button(top, image = send_button_photo)
            send_button.bind('<Button-1>', send_message_to_server)
            send_button.place(relx=0.87, rely=0.8)

            bottom_button_photo = PhotoImage(file="pics/bottoms.png")
            bottom_button = tk.Button(top, image = bottom_button_photo)
            bottom_button.bind('<Button-1>', bottom_bar_action)
            bottom_button.place(relx=0.01, rely=0.8)
            
            font_bar_photo = PhotoImage(file="pics/Fontbar.png")
            font_bar = tk.Button(top, image = font_bar_photo)
            font_bar.bind('<Button-1>', font_bar_action)
            font_bar.place(relx=0.02, rely=0.475)
            
            menubar = Menu(top)
            filemenu = Menu(menubar, tearoff=0)
            filemenu.add_command(label="Insert", command=donothing)
            filemenu.add_command(label="People", command=donothing)
            filemenu.add_command(label="Snapshot", command=donothing)
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=top.quit)
            menubar.add_cascade(label="File", menu=filemenu)

            helpmenu = Menu(menubar, tearoff=0)
            helpmenu.add_command(label="Help Index", command=donothing)
            helpmenu.add_command(label="About...", command=about_me)
            menubar.add_cascade(label="Help", menu=helpmenu)

            top.config(menu=menubar)

            top.mainloop()
        else:
            failed_label = tk.Label(canvas, text='Incorrect Password! or Account Doesn\'t Exist!', font=('Helvetica', 7), bg=GRAY)
            failed_label.place(relx=0.07, rely=0.8, relheight=0.05, relwidth=0.7)
            failed_count = 1
    else:
        failed_label = tk.Label(canvas, text='Incorrect Password! or Account Doesn\'t Exist!', font=('Helvetica', 7), bg=GRAY)
        failed_label.place(relx=0.07, rely=0.8, relheight=0.05, relwidth=0.7)
        failed_count = 1

image = Image.open("pics/theguy.png")
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


password_entry = tk.Entry(canvas, bg='white')
password_entry.bind('<Return>', open_server)
password_entry.config(show="*")                 # makes it do the ****** for passwords
password_entry.place(relx=0.095, rely=0.75, relheight=0.05, relwidth=0.8)

username_label = tk.Label(canvas, text='ScreenName', font=('helvetica', 12, 'bold'), bg=GRAY, fg='#2a2e7a')
username_label.place(relx=0.09, rely=0.55)

password_label = tk.Label(canvas, text='Password', font=('helvetica', 10, 'bold'), bg=GRAY, fg='black')
password_label.place(relx=0.09, rely=0.7)

create_account = tk.Button(canvas, text='Create Account!')
create_account.bind('<Button-1>', usr_create)
create_account.place(relx=0.1, rely=0.9, relheight=0.05, relwidth=0.5)


root.mainloop()

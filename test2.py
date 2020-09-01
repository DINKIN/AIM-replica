import tkinter as tk
from tkinter import colorchooser

root = tk.Tk()

txt = tk.Text(root)
txt.pack()

my_username = 'Anthony'
user_chat_info = 'Hello World'
incomming_username = 'Savannah'
incomming_message = 'Hi Babe!' 

chosen_color = ''

def something():
    chosen_color = colorchooser.askcolor()[1]


def send(new_color):
    txt.tag_config('sender', background="white", foreground="blue")
    txt.tag_config('messagecolor', background='white', foreground=new_color)
    txt.insert('end', my_username + ': ', 'sender')
    txt.insert('end', user_chat_info + '\n', 'messagecolor')

button = tk.Button(root, text='color me', command=something)
button.pack()

button = tk.Button(root, text='send me', command=send(chosen_color))
button.pack()







txt.tag_config('receiver', background="white", foreground="red")
txt.insert('end', incomming_username + ': ', 'receiver', incomming_message + '\n')






root.mainloop()
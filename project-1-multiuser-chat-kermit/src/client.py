'''
CS 3700 - Networking & Distributed Computing - Fall 2025
Instructor: Thyago Mota
Student(s): Andrew Stephens, Oliver Yang
Description: Project 1 - Multiuser Chat: Client
'''

from socket import *
from struct import pack
from datetime import datetime
import tkinter as tk
from tkinter import *
from threading import Thread, Semaphore
import sys
from random import randint

# "constants"
MCAST_ADDR  = '224.1.1.1'
MCAST_PORT  = 2241
SERVER_PORT = 4321
BUFFER      = 1024
GEOMETRY    = '570x400'

# the semaphore!
s = Semaphore(1)

class Window(Tk):
    def __init__(self,w,h,x,y,color, txtcolor, server_addr):
        super().__init__()

        # TODO #3 create the unicast UDP socket to send messages to the server
        self.send = socket(AF_INET, SOCK_DGRAM)

        # TODO #4 save the server address in an instance variable
        self.server_address = (server_addr, SERVER_PORT)

        # TODO #5 build the GUI 
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.geometry(f'{w}x{h}+{x}+{y}')

        self.tk.call('tk', 'scaling', 1.4)
                          
        self.resizable(100, 100)
        self.configure(bg=color)

        self.label = Label(self, text="Message:", bg=color)
        self.label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.message = Entry(self, bg=color, fg=txtcolor)
        self.message.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.text = Text(self, height=10, bg=color, fg=txtcolor)
        self.text.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)  
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        timestamp = datetime.now().strftime('%H:%M:%S')
        tim = f"[{timestamp}]"

        self.title(f"Time: {tim}\t\t CS3700: A Multiuser Chat ")
        self.bind('<Return>', self.enter)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.message.focus_set()

    # TODO #6 read the input text field, update the text box, and send the message to the server using the unicast UDP socket
    def enter(self, event):
        timestamp = datetime.now().strftime('%H:%M:%S')
        tim = f"[{timestamp}]"
        msg = self.message.get()
        self.text.insert('1.0', f"-> {tim}\t{msg}\n")
        self.text.see('1.0')  
        self.message.delete(0, 'end')
        self.send.sendto(f'{msg}'.encode(), self.server_address)
        pass

    # TODO #7 updated the text box avoiding race conditions
    def update(self, msg):  
        s.acquire()
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            tim = f"[{timestamp}]"
            self.text.insert('1.0', f"<- {tim}\t{msg}\n")
            self.text.see('1.0')
        finally:
            s.release()
        pass
    
    def exit(self):
        try:
            self.send.sendto(f"exit,".encode(), self.server_address)
        except:
            pass
        self.destroy()
        sys.exit(0)

class FromServerThread(Thread): 

    def __init__(self, window): 
        Thread.__init__(self)

        # TODO #8 create the mcast UDP socket to receive messages from the server; bind the socket to MCAST_PORT
        self.from_serv = socket(AF_INET, SOCK_DGRAM)
        self.from_serv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.from_serv.bind(('', MCAST_PORT))
        
        # formats MCAST_ADDR to a network format
        group = inet_aton(MCAST_ADDR) 
        # formats the multicast group into a multicast request structure (mreq)
        mreq = pack('4sL', group, INADDR_ANY)
    
        # TODO #9 configure the socket to read from the multicast group; uncomment and make changes in the line below based on how you named your socket's variable
        self.from_serv.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

        # TODO #10 save the window reference in an instance variable 
        self.window = window

    # TODO #11 read from the socket and update the window's text box
    def run(self): 
        while True:
            try:
                data, _ = self.from_serv.recvfrom(BUFFER)
                msg = data.decode()
                self.window.update(msg)
            except Exception as e:
                print(f"Receiver error: {e}")
                break
            
if __name__ == '__main__': 
    if len(sys.argv) <= 1: 
        print(f'Use: {sys.argv[0]} server_address')
        sys.exit(1)
    server_addr = sys.argv[1].lower()
    w = str(input('Width:? '))
    h = str(input('Height? '))
    c = str(input('Background Color? '))
    txtcolor = str(input('Text Color? '))
    server_addr = str(input('Server Address? '))
   
    for _ in range(10):
        x = randint(0, 1024)
        y = randint(0, 768)
        window = Window(w, h, x, y, c, txtcolor, server_addr)
        from_server_thread = FromServerThread(window)
        from_server_thread.start()
        window.mainloop()




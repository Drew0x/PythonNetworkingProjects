'''
CS 3700 - Networking & Distributed Computing - Fall 2025
Instructor: Thyago Mota
Student(s): Andrew Stephens, Oliver Yang
Description: Project 1 - Multiuser Chat: Server
'''

from socket import socket, AF_INET, SOCK_DGRAM, IPPROTO_IP, IP_MULTICAST_TTL
from datetime import datetime
import struct

# "constants"
MCAST_ADDR  = '224.1.1.1'
MCAST_PORT  = 2241
SERVER_ADDR = '0.0.0.0'
SERVER_PORT = 4321
BUFFER      = 1024

if __name__ == '__main__':

    users = {}
    # TODO #1 create the 2 sockets: one to receive messages from the clients and another one to send messages to the clients (using the mcast group:port); make sure the socket that receives messages is bound to (SERVER_ADDR, SERVER_PORT)
    # Receiving socket (server listens here)
    rcv_sock = socket(AF_INET, SOCK_DGRAM)
    rcv_sock.bind((SERVER_ADDR, SERVER_PORT))

    # Sending socket (multicast)
    sck = socket(AF_INET, SOCK_DGRAM)
    sck.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, struct.pack('b', 1))

    # TODO #2 implement the communication protocol
    print(f"Multiuser server is ready on {SERVER_ADDR}:{SERVER_PORT}!")

    while True:
        data, client_addr = rcv_sock.recvfrom(BUFFER)
        message = data.decode().strip()
        timestamp = datetime.now()

        # LOGIN
        if message.startswith("login,"):
            username = message.split(",")[1].strip()
            users[username] = client_addr
            sck.sendto(f"welcome, {username}".encode(), (MCAST_ADDR, MCAST_PORT))
            print(f"{timestamp} login request has arrived from {username}@{client_addr}")

        # MSG
        elif message.startswith("msg,"):
            msg_content = message.split(",", 1)[1].strip()
            username = next((u for u, a in users.items() if a == client_addr), None)
            if username:
                #sck.sendto(f"msg, {username}: {msg_content}".encode(), (MCAST_ADDR, MCAST_PORT))
                sck.sendto(f"msg, {msg_content}".encode(), (MCAST_ADDR, MCAST_PORT))
                print(f"{timestamp} msg \"{msg_content}\" has arrived from user: {username}@{client_addr}")

        # EXIT
        elif message.startswith("exit,"):
            username = next((u for u, a in users.items() if a == client_addr), None)
            if username:
                users.pop(username, None)
                sck.sendto(f"bye, {username}".encode(), (MCAST_ADDR, MCAST_PORT))
                print(f"{timestamp} exit request from {username}@{client_addr}")

        # LIST
        elif message.startswith("list,"):
            username = next((u for u, a in users.items() if a == client_addr), None)
            user_list = "{" + ", ".join([f"{addr}: '{u}'" for u, addr in users.items()]) + "}"
            sck.sendto(f"list, {user_list}".encode(), (MCAST_ADDR, MCAST_PORT))
            print(f"{timestamp} list request has arrived from user: {username}@{client_addr}")




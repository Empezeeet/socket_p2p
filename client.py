
import socket 
import base64
import os
import threading
import time


def getmyIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    myIP = (s.getsockname()[0])
    s.close()
    del s
    return str(myIP)
IP = getmyIP()
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'    
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER_INPUT = f"192.168.0.{input('[CLIENT] Enter SERVER IP > 192.168.0.')}"

SERVER = SERVER_INPUT
ADDR = (SERVER, PORT)
COMMANDS = ["!CLEAR", "!PCON", "!BROADCAST"]


try:
    print("[CLIENT] Creating Socket", end="\r")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("Can't establish connection with server (err_wroip).")
    breakpoint()


def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

def encodeText(text):
    return base64.b64encode(text.encode()).decode('ascii')
def decodeText(text):
    return base64.b64decode(text).decode('ascii')

def checkForMSG():
    recvIP = client.recv(2048).decode(FORMAT)
    recvMSG = client.recv(4096).decode(FORMAT)
    if recvIP == IP:
        print(recvMSG)
try:
    print("[CLIENT] Connecting to SERVER", end="\r")
    client.connect(ADDR)
except ConnectionRefusedError:
    print("Can't establish connection with server (err_connref).")
    input("Press enter to exit...")
    exit()
send(socket.gethostname())
firstIteration = True
shouldCheckForMSG = False
print(f"<================[  CONNECTED TO SERVER  ]================>")
print(f"<================[  IP:  {IP}   ]================>")






while True:

    if firstIteration is False and shouldCheckForMSG is True:
        checkForMSG()
    if firstIteration is False:
        for x in range(0, 4):
            
            b = " [CLIENT] Cooldown" + "." * x
            print(b, end="\r")
            time.sleep(1)
        print("")
    msg = input("> ")

        

    if msg[0] == "!":
        if msg == DISCONNECT_MESSAGE:
            send(msg)
            print(f"<================[  DISCONNECTING  ]================>")
            print(f"<================[     GOODBYE     ]================>")
            break
        if msg == COMMANDS[0]: # / !CLEAR
            print("\n" * 100)
            firstIteration = True
            print("[CLIENT] Cleared screen.")
        if msg == COMMANDS[1]: # / !PCON
            send(msg)
            print(client.recv(4096).decode(FORMAT))
        if msg == COMMANDS[2]: # / !BROADCAST
            send(msg)
            print("[CLIENT] Broadcasting...")
        
        shouldCheckForMSG = False
        continue
    # Check if message is only spaces
    elif msg.isspace():
        print("[CLIENT] Message cannot be empty.")
        shouldCheckForMSG = False
        continue
    elif msg[0] != "!":
        if len(msg) > 128:
            print("[CLIENT] Message is too long.")
            shouldCheckForMSG = False
            continue
        send(msg)
        firstIteration = False
        shouldCheckForMSG = True















import socket
import threading
import random


def getmyIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    myIP = (s.getsockname()[0])
    s.close()
    del s
    return myIP
HEADER = 64
PORT = 5050
SERVER = str(getmyIP())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'    
DISCONNECT_MESSAGE = "!DISCONNECT"
PCON_MESSAGE = "!PRINT_CONN"

ip_to_name = {
    # Example
    # "192.168.0.100": "UserComputer.local"
}

connections = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



def handle_client(conn, addr):
    
    connections.append(conn)
    connected = True
    hostname_lenght = conn.recv(HEADER).decode(FORMAT)
    if hostname_lenght:
        hostname_lenght = int(hostname_lenght)
        hostname = conn.recv(hostname_lenght).decode(FORMAT)
    ip_to_name[addr[0]] = hostname[:-6]
    print(f"[NEW CONNECTION] {ip_to_name[addr[0]]}@{addr[0]} connected.")
    while connected:
        msg_lenght = conn.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = conn.recv(msg_lenght).decode(FORMAT)
            if msg[0] != "!":
                print(f"[{addr[0]} @ {addr[1]}]: {msg}")
                for connection in connections:
                    #if connection == conn:
                    connection.send(str(addr[0]).encode(FORMAT))
                    connection.send(f"[ {str(ip_to_name[addr[0]]).upper()}@{addr[0]} ]: {msg}".encode(FORMAT))
            if msg == DISCONNECT_MESSAGE:
                connected = False
                for connection in connections:
                    connection.send(f"[SERVER] {addr[0]} disconnected.".encode(FORMAT))
                connections.remove(conn)
                print(f"[ {str(ip_to_name[addr[0]]).upper()}@{addr[0]} ] Disconnected.")
            if msg == PCON_MESSAGE:
                conn.send(f"CONNECTIONS: {str(len(connections))}".encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print(f"<================[  INITIALIZED SERVER @ v1.1  ]================>")
    print(f"<================[  SERVER IP:  {SERVER}  ]================>")
    print(f"[LISTENING] Waiting for connections...")
    while True:
        
        conn, addr = server.accept()
        ConnectedClient = threading.Thread(target=handle_client, args=(conn, addr), name=f"Client{random.randint(100, 999)}")
        ConnectedClient.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print(f"[STARTING] Server is starting...")
start()














import socket
import threading

HEADER = 16
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 1234
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))


def handle_client(connection, address): 
    print(f"[NEW CONNECTION] {address} connected.")

    connected = True
    while connected:
        msg_length = connection.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{address}] {msg}")

    print(f"\n[DISCONNECTING] {address} disconnected")
    connection.close()
    # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}\n")


def start():
    server.listen()
    print(f"[LISTENING] Server listening on {SERVER}")
    while True:
        print(f"first [ACTIVE CONNECTIONS] {threading.activeCount() -1}")
        connection, address = server.accept()
        thread = threading.Thread(
            target=handle_client, args=(connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")


print("[STARTING] Server is starting...")
start()

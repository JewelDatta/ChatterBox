import socket
from threading import Thread
from client import Client
from datetime import datetime


HOST = socket.gethostbyname(socket.gethostname())
PORT = 1234
HEADER = 12
MAX_CONNECTIONS = 5
SERVER = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
FORMAT = "utf-8"


clients = []


def broadcast(msg, name):
    """
    send message to all the clients

    Args:
        msg (str): message to be send
        name (sr): name of sender
    """
    msg = (name+msg).encode(FORMAT)
    msg_length = len(msg)

    for client in clients:
        connection = client.connection
        try:
            msg_length = str(msg_length).encode(FORMAT)
            msg_length += b' ' * (HEADER-len(msg_length))

            connection.send(msg_length)
            connection.send(msg)
        except Exception as e:
            print("[EXCEPTION]", e)
            print(f"Couldn't pass the message to {client.name}")


def client_communication(client):
    """
    This thread handle all incoming messages from clients

    Args:
        client (Client): holds information about client
    """

    connection = client.connection

    # first message received is always the persons name

    name_length = connection.recv(HEADER).decode(FORMAT)
    name_length = int(name_length)
    name = connection.recv(name_length).decode(FORMAT)
    client.set_name(name)

    msg = f"{name} has joined the chat!"
    print(msg)

    broadcast(msg, "")  # broadcast welcome message

    while True:  # wait for any messages from person
        msg_length = connection.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT)

            if msg == "{quit}":  # if message is qut disconnect client
                connection.close()
                clients.remove(client)
                broadcast(f"{name} has left the chat...", "")
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:  # otherwise send message to all other clients
                # print(f"\n for {name} and message is {msg}\n")
                broadcast(msg, name+": ")
                print(f"{name}::::::::::: ", msg)


def accept_incoming_connnection():
    while True:
        try:
            connection, address = SERVER.accept()  # wait for any new connections

            # create Client object for connection
            client = Client(connection, address)
            clients.append(client)
            print(
                f"[CONNECTION] {address} connected to the server at {datetime.now()}")
            Thread(target=client_communication, args=(client,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)
    print("[STARTED] waiting for connections...")
    accept_thread = Thread(target=accept_incoming_connnection)
    accept_thread.start()
    accept_thread.join()
    SERVER.close()

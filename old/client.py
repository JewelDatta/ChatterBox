import socket


HEADER = 16
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 1234
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)

# input()
# send("Hello world")
# input()
# send("welcome everyone")
# input()
# send(DISCONNECT_MESSAGE)


if __name__ == "__main__":
    cnt = 5
    while cnt:
        cnt -= 1
        msg = input()
        send(msg)

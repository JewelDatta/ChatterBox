import socket
from threading import Thread, Lock
import time


class Client:
    """
    for communicating with server
    """
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 1234
    FORMAT = 'utf-8'
    HEADER = 12

    def __init__(self, name):
        """
        Init object and send name to server
        :param name: str
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()

    def receive_messages(self):
        """
        receive messages from server
        :return: None
        """
        while True:
            try:
                msg_length = self.client_socket.recv(self.HEADER).decode()
                msg_length = int(msg_length)
                
                msg = self.client_socket.recv(msg_length).decode()

                # make sure memory is safe to access(thread sycronization)
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCPETION]", e)
                break

    def send_message(self, msg):
        """
        send messages to server
        :param msg: str
        :return: None
        """
        try:
            msg = msg.encode(self.FORMAT)
            msg_length = len(msg)
            msg_length = str(msg_length).encode(self.FORMAT)
            msg_length += b' ' * (self.HEADER-len(msg_length))

            self.client_socket.send(msg_length)
            self.client_socket.send(msg)

            if msg.decode(self.FORMAT) == "{quit}":
                self.client_socket.close()
        except Exception as e:
            # self.client_socket = socket(AF_INET, SOCK_STREAM)
            # self.client_socket.connect(self.ADDR)
            print(e)

    def get_messages(self):
        """
        :returns a list of str messages
        :return: list[str]
        """
        messages_copy = self.messages[:]

        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")

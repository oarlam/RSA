import socket
import threading
from rsa import RSA, XOR
import hashlib

class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        self.rsa = RSA()
        self.secret_key = "secretkey"

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username
            self.clients.append(c)

            # send public key to the client
            c.send(f"{self.rsa.e},{self.rsa.n}".encode())

            client_public = c.recv(1024).decode()
            e, n = client_public.split(',')
            client_public = (int(e), int(n))

            # encrypt the secret with the clients public key
            encrypted_secret = self.rsa.encrypt(self.secret_key, client_public)

            # send the encrypted secret to a client
            c.send(str(encrypted_secret).encode())

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:

            # encrypt the message

            encrypted_msg = XOR.encrypt(msg, self.secret_key)
            client.send(encrypted_msg.encode())

    def handle_client(self, c: socket, addr):
        while True:
            try:
                msg = c.recv(1024)
                if not msg:
                    break
                for client in self.clients:
                    if client != c:
                        client.send(msg)
            except ConnectionResetError:
                self.clients.remove(c)
                break

if __name__ == "__main__":
    s = Server(9001)
    s.start()

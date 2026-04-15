import socket
import threading
from rsa import RSA, XOR

class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        # create key pairs
        self.rsa = RSA()

        # exchange public keys
        server_key = self.s.recv(1024).decode()
        e, n = server_key.split(',')
        self.server_public = (int(e), int(n))
        self.s.send(f"{self.rsa.e},{self.rsa.n}".encode())

        # receive the encrypted secret key
        secret_key_encrypt = int(self.s.recv(1024).decode())
        self.secret_key = self.rsa.decrypt(secret_key_encrypt)

        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self):
        while True:
            message = self.s.recv(1024).decode()
            if not message:
                break

            # decrypt message with the secrete key
            decrypted_message = XOR.decrypt(message, self.secret_key)
            print(decrypted_message)


    def write_handler(self):
        while True:
            message = input()
            msg = f"[{self.username}]: {message}"

            # encrypt message with the secrete key

            encrypted_message = XOR.encrypt(msg, self.secret_key)
            self.s.send(encrypted_message.encode())

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()

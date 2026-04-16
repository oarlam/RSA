import socket
import threading
from encription import RSA, XOR
import hashlib
import random

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

            try:
                received_hash, message = message.split('||')
            except ValueError:
                print('[ERROR] The recieved message had an error')
                continue

            # decrypt message with the secrete key
            decrypted_message = XOR.decrypt(message, self.secret_key)
            calculated_hash = hashlib.sha3_512(decrypted_message.encode('utf-8')).hexdigest()

            if calculated_hash == received_hash:
                print(decrypted_message)
            else:
                print('[ERROR] The recieved message had an error')


    def write_handler(self):
        while True:
            message = input()
            msg = f"[{self.username}]: {message}"
            msg_hash = hashlib.sha3_512(msg.encode('utf-8')).hexdigest()

            # encrypt message with the secrete key

            encrypted_message = XOR.encrypt(msg, self.secret_key)
            both = msg_hash + '||' + encrypted_message
            self.s.send(both.encode())

if __name__ == "__main__":
    NAMES = ['ivan', 'marti', 'kely', 'ben', 'kate', 'julie']
    name = random.choice(NAMES)
    cl = Client("127.0.0.1", 9001, name)
    cl.init_connection()

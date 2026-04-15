'''rsa'''
from random import randrange

class RSA:
    '''rsa'''
    def __init__(self):
        self.e = 65537
        self.p = None
        self.q = None
        self.get_p_and_q()

        self.n = self.p * self.q

        self.phi = (self.p - 1) * (self.q - 1)

        self.d = pow(self.e, -1, self.phi)

    def is_prime(self, num):
        '''Тест Міллера — Рабіна'''
        if num % 2 == 0:
            return False
        d = num - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        def trial_composite(a):
            if pow(a, d, num) == 1:
                return False
            for i in range(s):
                if pow(a, 2**i * d, num) == num-1:
                    return False
            return True

        for _ in range(50):
            a = randrange(2, num)
            if trial_composite(a):
                return False
        return True

    def get_p_and_q(self):
        '''p та q'''
        while True:
            p = randrange(10**100, 10**150)
            if self.is_prime(p) and (p-1) % self.e != 0:
                self.p = p
                break
        while True:
            q = randrange(10**100, 10**150)
            if self.is_prime(q) and self.p != q and (q-1) % self.e != 0:
                self.q = q
                break

    def get_public_key(self):
        '''public key'''
        return self.e, self.n

    def encrypt(self, message, public_key):
        '''ecrypt'''
        e, n = public_key
        byte = message.encode('utf-8')
        ints = int.from_bytes(byte, byteorder='big')
        return pow(ints, e, n)

    def decrypt(self, ciphered):
        '''decrypt'''
        ints = pow(ciphered, self.d, self.n)
        byte_length = (ints.bit_length() + 7) // 8
        byte = ints.to_bytes(byte_length, byteorder='big').decode('utf-8')
        return byte


class XOR:
    '''xor'''
    @staticmethod
    def decrypt(msg, secret_key):
        '''decrypt'''
        key_bytes = secret_key.encode('utf-8')
        cipher_bytes = bytes.fromhex(msg)

        plain_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(cipher_bytes)])

        return plain_bytes.decode('utf-8')

    @staticmethod
    def encrypt(msg, secret_key):
        '''encrypt'''
        key_bytes = secret_key.encode('utf-8')
        plain_bytes = msg.encode('utf-8')

        cipher_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(plain_bytes)])

        return cipher_bytes.hex()

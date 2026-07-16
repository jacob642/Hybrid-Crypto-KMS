""""
Hybrid encryption/decryption using Fernet (AES-128-CBC + HMAC-SHA256) + RSA-OAEP.
This file handles ONLY crypto logic — no user input, no logging.
"""

import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet, InvalidToken

KEYS_DIR = "keys"


def generate_rsa_keys():
    os.makedirs(KEYS_DIR, exist_ok=True)
    if os.path.isfile(f"{KEYS_DIR}/private.pem"):
        private_key = RSA.import_key(open(f"{KEYS_DIR}/private.pem", "rb").read())
        public_key = RSA.import_key(open(f"{KEYS_DIR}/public.pem", "rb").read())
    else:
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        with open(f"{KEYS_DIR}/private.pem", "wb") as f:
            f.write(private_key)
        with open(f"{KEYS_DIR}/public.pem", "wb") as f:
            f.write(public_key)
    return private_key, public_key


def byte_to_hex(message: str) -> str:
    return message.encode("utf-8").hex().upper()


def encryption(message: str, fernet_key: bytes) -> tuple[bytes, bytes]:
    with open(f"{KEYS_DIR}/public.pem", "rb") as pem_file:
        public_key = RSA.import_key(pem_file.read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(fernet_key)
    fernet = Fernet(fernet_key)
    token = fernet.encrypt(message.encode("utf-8"))
    return encrypted_key, token


def decryption(token: bytes, encrypted_key: bytes) -> str:
    with open(f"{KEYS_DIR}/private.pem", "rb") as pem_file:
        private_key = RSA.import_key(pem_file.read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    fernet_key = cipher_rsa.decrypt(encrypted_key)
    fernet = Fernet(fernet_key)
    try:
        return fernet.decrypt(token).decode("utf-8")
    except InvalidToken:
        raise ValueError("Decryption failed: wrong key or corrupted data.")
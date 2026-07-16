import logging

from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates

from Hybrid_AES_RSA import encryption, decryption, generate_rsa_keys, byte_to_hex
from KMS import KeyManager
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


def main() -> None:
    # set up KMS first
    kms = KeyManager()
    kms.setup()

    # generate RSA keys
    generate_rsa_keys()

    # generate fernet session key and store it in KMS
    fernet_key = Fernet.generate_key()
    kms.store_key("fernet_key", fernet_key)

    # get message from user
    message = input("Please enter the message you would like to send: ")

    # encrypt
    encrypted_key, token = encryption(message, fernet_key)

    # decrypt — load key back from KMS
    try:
        stored_key = kms.load_key("fernet_key")
        decrypted = decryption(token, encrypted_key)
        logger.info("Decrypted message: %s", decrypted)
    except ValueError as e:
        logger.error(str(e))

    # prove load works
    loaded = kms.load_key("fernet_key")
    print("Keys match:", loaded == fernet_key)

    # rotate master key
    kms.rotate()

    # revoke the key
    questionr = input("Please enter yes if you want to revoke key: ")
    if questionr == "yes":
        kms.revoke("fernet_key")
        try:
            kms.load_key("fernet_key")
        except KeyError as e:
            print("Key successfully revoked:", e)
    else:
        print("Key will not be revoked")


if __name__ == "__main__":
    main()
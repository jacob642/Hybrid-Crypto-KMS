# KMS for the keys used
import os
import json
import logging
from cryptography.fernet import Fernet
from datetime import datetime


class KeyManager:
    def __init__(self):
        # paths
        self.keys_dir = os.path.join(os.getcwd(), "KMS")
        self.keystore_path = os.path.join(self.keys_dir, "keystore.enc")
        self.master_key_path = os.path.join(self.keys_dir, "master.key")
        self.metadata_path = os.path.join(self.keys_dir, "metadata.json")
        self.logger = None  # set up in setup() once KMS/ folder exists

    def setup(self):
        # create KMS folder if it doesn't exist
        if os.path.isdir(self.keys_dir):
            pass
        else:
            os.makedirs(self.keys_dir)

        # logging points to KMS/audit.log
        logging.basicConfig(
            level=logging.INFO,
            format="{asctime} - {levelname} - {funcName} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
            handlers=[
                logging.FileHandler(os.path.join(self.keys_dir, "audit.log"), encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("KMS")
        self.logger.info("KMS setup started")

        # check master key
        if os.path.isfile(self.master_key_path):
            self.logger.info("Master key exists")
        else:
            self.logger.info("[SETUP] No master key found - generating one")
            master_key = Fernet.generate_key()
            with open(self.master_key_path, "wb") as f:
                f.write(master_key)

        # check keystore
        if os.path.isfile(self.keystore_path):
            self.logger.info("Key store file exists")
        else:
            self.logger.info("[SETUP] No key store found - creating one")
            self._save_keystore({})

        # check metadata
        if os.path.isfile(self.metadata_path):
            self.logger.info("Metadata file exists")
        else:
            self.logger.info("[SETUP] No metadata found - creating one")
            with open(self.metadata_path, "w") as f:
                json.dump({}, f)

        self.logger.info("[SETUP] KMS setup complete")

    # load master key from disk
    def _load_master_key(self) -> bytes:
        with open(self.master_key_path, "rb") as f:
            return f.read()

    # encrypt and save keystore to disk
    def _save_keystore(self, data: dict):
        master_key = self._load_master_key()
        fernet = Fernet(master_key)
        encrypted = fernet.encrypt(json.dumps(data).encode("utf-8"))
        with open(self.keystore_path, "wb") as f:
            f.write(encrypted)

    # decrypt and load keystore from disk
    def _load_keystore(self) -> dict:
        master_key = self._load_master_key()
        fernet = Fernet(master_key)
        with open(self.keystore_path, "rb") as f:
            decrypted = fernet.decrypt(f.read())
        return json.loads(decrypted.decode("utf-8"))

    def store_key(self, key_name: str, key_data: bytes):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # update metadata
        with open(self.metadata_path, "r") as f:
            metadata = json.load(f)
        metadata[key_name] = {
            "created_at": now,
            "status": "active"
        }
        with open(self.metadata_path, "w") as f:
            json.dump(metadata, f)
        # store key
        keystore = self._load_keystore()
        keystore[key_name] = key_data.hex()
        self._save_keystore(keystore)
        self.logger.info("[STORE] key=%s status=success", key_name)

    def load_key(self, key_name: str) -> bytes:
        keystore = self._load_keystore()
        if key_name not in keystore:
            self.logger.error("[ACCESS] key=%s status=failed reason=key not found", key_name)
            raise KeyError(f"Key '{key_name}' not found in keystore")
        # update only last_accessed
        with open(self.metadata_path, "r") as f:
            metadata = json.load(f)
        metadata[key_name]["last_accessed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.metadata_path, "w") as f:
            json.dump(metadata, f)
        self.logger.info("[ACCESS] key=%s status=success", key_name)
        return bytes.fromhex(keystore[key_name])

    def revoke(self, key_name: str):
        keystore = self._load_keystore()
        if key_name not in keystore:
            self.logger.error("[REVOKE] key=%s status=failed reason=key not found", key_name)
            raise KeyError(f"Key '{key_name}' not found in keystore")
        # update metadata before deleting
        with open(self.metadata_path, "r") as f:
            metadata = json.load(f)
        metadata[key_name]["date_revoked"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata[key_name]["status"] = "revoked"
        with open(self.metadata_path, "w") as f:
            json.dump(metadata, f)
        # delete from keystore
        del keystore[key_name]
        self._save_keystore(keystore)
        self.logger.warning("[REVOKE] key=%s status=success", key_name)

    def rotate(self):
        # load existing keystore with old master key
        keystore = self._load_keystore()
        # generate new master key and save it
        new_master_key = Fernet.generate_key()
        with open(self.master_key_path, "wb") as f:
            f.write(new_master_key)
        # re-encrypt keystore with new master key
        self._save_keystore(keystore)
        self.logger.warning("[ROTATE] status=success")

    def import_key(self, key_name: str, key_data: bytes):
        self.store_key(key_name, key_data)
        self.logger.info("[IMPORT] key=%s status=success", key_name)

    def export(self, key_name: str) -> bytes:
        key = self.load_key(key_name)
        self.logger.info("[EXPORT] key=%s status=success", key_name)
        return key
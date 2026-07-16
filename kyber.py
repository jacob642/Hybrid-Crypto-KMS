from kyber_py.ml_kem import ML_KEM_768
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

# Kyber produces a shared SECRET, not a cipher — so we derive an AES key from it
# and use AES-GCM to actually encrypt the data. This is the standard pattern.

def derive_aes_key(shared_secret: bytes) -> bytes:
    """
    Hash the Kyber shared secret with SHA-256 to produce a clean 32-byte AES key.
    This is recommended because raw KEM output should always be hashed before
    use as a symmetric key (provides better domain separation and uniformity).
    """
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(shared_secret)
    return digest.finalize()  # Always 32 bytes (256-bit AES key)


# ── RECIPIENT: generate keypair ───────────────────────────────────────────────
ek, dk = ML_KEM_768.keygen()
# ek is shared with the sender (e.g. stored in a certificate or profile)
# dk is stored securely by the recipient

# ── SENDER: encapsulate + encrypt ────────────────────────────────────────────
shared_secret_sender, kem_ciphertext = ML_KEM_768.encaps(ek)
# Derive a 256-bit AES key from the shared secret
aes_key_sender = derive_aes_key(shared_secret_sender)

# AES-GCM needs a unique 12-byte nonce each time — never reuse a nonce with the same key
nonce = os.urandom(12)

# Encrypt the actual message with AES-256-GCM
# AES-GCM also provides authentication (detects tampering), unlike plain AES-CBC
aesgcm = AESGCM(aes_key_sender)
encrypted_data = aesgcm.encrypt(nonce, b"Top secret message", None)
# None = no additional authenticated data (AAD); you can pass metadata here if needed

# Sender transmits: kem_ciphertext + nonce + encrypted_data

# ── RECIPIENT: decapsulate + decrypt ─────────────────────────────────────────
# Recover the shared secret using the private key
shared_secret_recipient = ML_KEM_768.decaps(dk, kem_ciphertext)
aes_key_recipient = derive_aes_key(shared_secret_recipient)

# Decrypt — will raise an exception if the data has been tampered with
decrypted = AESGCM(aes_key_recipient).decrypt(nonce, encrypted_data, None)

print(decrypted)  # b'Top secret message'
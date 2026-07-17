# Hybrid-Crypto-KMS

A compact, hands-on Key Management Service (KMS) and hybrid encryption demo written in Python. Built during an internship to deepen my practical understanding of applied cryptography, this project demonstrates envelope encryption (RSA-OAEP wrapping of Fernet session keys), a local encrypted keystore, and basic key lifecycle operations such as rotation and revocation. It is designed for learning and portfolio use.

## Project Overview

Hybrid-Crypto-KMS is an educational implementation that shows how common key management patterns map to working code. The project focuses on clarity and separation of concerns so you can follow the cryptographic flow and the keystore lifecycle without getting lost in infrastructure details.

### Core ideas demonstrated

- Envelope encryption with RSA-OAEP for key wrapping and Fernet for authenticated symmetric encryption.
- A local KMS that stores keys encrypted under a master key and tracks metadata for auditing.
- Key lifecycle operations including generate, import/export, rotate, and revoke.
- Clean separation between crypto primitives and key management logic.

## Features

- Hybrid encryption using RSA for key encryption and Fernet for message encryption.
- Encrypted keystore protected by a master key stored on disk.
- Metadata and audit logging for creation time, last access, and revocation events.
- Key rotation that replaces the master key and re-encrypts the keystore.
- Key revocation that marks keys as revoked and removes them from the keystore.
- Minimal CLI demo to exercise encrypt, decrypt, rotate, and revoke flows.

## Quick Start

Clone the repository:

```bash
git clone <repo-url>
cd Hybrid-Crypto-KMS
```

Create and activate a virtual environment.

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the demo:

```bash
python main.py
```

### Try the following

- Enter a message to encrypt.
- Verify decryption using the stored key.
- Rotate the master key and confirm the keystore is re-encrypted.
- Revoke a key and confirm it can no longer be loaded.

## Usage Examples

### Encrypt a message

Run `python main.py`, enter a message, and the application will generate an encrypted token along with an RSA-wrapped Fernet key.

### Decrypt a message

The demo loads the wrapped key from the keystore and decrypts the message using the RSA private key and recovered Fernet key.

### Rotate the master key

Use the rotation option to generate a new master key and re-encrypt the keystore.

### Revoke a key

Revoke a stored key and verify that future attempts to load it raise an error.

## Improvements & Next Steps

Some practical improvements that could be made in the future include:

- Replace RSA with a post-quantum KEM such as Kyber (ML-KEM).
- Use HKDF for key derivation when using a KEM.
- Add support for algorithm negotiation and migration between RSA and post-quantum encryption.
- Store the master key in an operating system keystore or HSM instead of a local file.
- Introduce role-based access controls.
- Expand audit logging with user identity and request information.
- Improve testing and CI/CD.
- Benchmark encryption performance.
- Add a migration guide and threat model documentation.

## Repository Structure

```text
Hybrid-Crypto-KMS/
├── README.md
├── main.py
├── Hybrid_AES_RSA.py
├── KMS/
│   ├── key_manager.py
│   ├── keystore.enc
│   ├── metadata.json
│   └── master.key
└── keys/
    ├── private.pem
    └── public.pem
```

## Important

The following files contain sensitive material and should **never** be committed:

- `KMS/master.key`
- `keys/private.pem`

Add them to your `.gitignore`.

## Tests

Recommended unit tests include:

- Keystore save/load using the master key.
- Store and retrieve keys through the KMS API.
- Master key rotation without data loss.
- Key revocation and metadata updates.
- Encryption/decryption round trips.
- Future migration tests for RSA → post-quantum KEM.

`pytest` is recommended for testing.


## Final Notes

This repository is intended as a learning project to explore hybrid encryption and key management in Python. It demonstrates how envelope encryption and basic KMS concepts work together in practice and provides a foundation for experimenting with more advanced cryptographic techniques in the future.

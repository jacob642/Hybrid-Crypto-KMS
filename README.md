Hybrid-Crypto-KMS
A compact, hands‑on Key Management Service and hybrid encryption demo written in Python. Built during an internship to deepen practical understanding of applied cryptography, this project demonstrates envelope encryption (RSA‑OAEP wrapping of Fernet session keys), a local encrypted keystore, and basic key lifecycle operations such as rotation and revocation. It is designed for learning and portfolio use.

Project Overview
Hybrid‑Crypto‑KMS is an educational implementation that shows how common key management patterns map to working code. The project focuses on clarity and separation of concerns so you can follow the cryptographic flow and the keystore lifecycle without getting lost in infrastructure details.

Core ideas demonstrated

Envelope encryption with RSA‑OAEP for key wrapping and Fernet for authenticated symmetric encryption.

A local KMS that stores keys encrypted under a master key and tracks metadata for auditing.

Key lifecycle operations including generate, import/export, rotate, and revoke.

Clean separation between crypto primitives and key management logic to make the design easy to read and test.

Features
Hybrid encryption using RSA for key encryption and Fernet for message encryption.

Encrypted keystore protected by a master key stored on disk.

Metadata and audit logging for creation time, last access, and revocation events.

Key rotation that replaces the master key and re‑encrypts the keystore.

Key revocation that marks keys as revoked and removes them from the keystore.

Minimal CLI demo to exercise encrypt, decrypt, rotate, and revoke flows.

Quick Start
Clone the repository and change into the project folder

bash
git clone <repo-url>
cd Hybrid-Crypto-KMS
Create and activate a virtual environment

bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows PowerShell
Install dependencies

bash
pip install -r requirements.txt
Run the demo CLI

bash
python main.py
Try the flows

Enter a message to encrypt.

Verify decryption using the stored key.

Rotate the master key and confirm the keystore re‑encrypts.

Revoke a key and confirm it can no longer be loaded.

Usage Examples
Encrypt a message  
Run python main.py, follow the prompt to enter a message, and note the encrypted token and wrapped key.

Decrypt a message  
The demo loads the wrapped key from the keystore and decrypts the token using the private RSA key and the unwrapped Fernet key.

Rotate master key  
Use the rotation option in the demo to generate a new master key and re‑encrypt the keystore contents.

Revoke a key  
Revoke a named key from the keystore and verify that subsequent load attempts raise an error.

Improvements & Next Steps
Below are concrete, practical improvements you can implement to modernize and harden the project. Each item includes why it helps and what to change in the codebase.

1. Replace RSA with a post‑quantum KEM (e.g., Kyber / ML‑KEM)
Why: RSA is vulnerable to future quantum attacks. A KEM (Key Encapsulation Mechanism) like Kyber provides post‑quantum security and is designed for key wrapping.
What to change

Key generation: replace RSA keypair generation with a Kyber (or other ML‑KEM) keypair. Use a well‑maintained PQC library (liboqs bindings, pyca/oqs if available, or pqcrypto wrappers).

Wrap/unwrap functions: change encryption() to use the KEM encapsulate API to produce an encapsulated key and shared secret; use the shared secret as the Fernet key (or derive a Fernet‑compatible key via HKDF). Change decryption() to decapsulate and derive the same symmetric key.

Key formats: store public/private KEM keys in a safe binary format; update keys/ layout and .gitignore.

Metadata: add a kdf and kem field to metadata so the keystore records which KEM/KDF was used for each entry.

Backward compatibility: add versioning to keystore entries (e.g., version: 1 for RSA, version: 2 for Kyber) and implement a migration path.

2. Use a KDF and key derivation best practices
Why: KEM shared secrets often need a KDF to produce symmetric keys of the right length and to add domain separation.
What to change

Use HKDF (with SHA‑256 or SHA‑3) to derive a Fernet‑compatible key from the KEM shared secret.

Include context info (algorithm id, key id) in HKDF info parameter.

Store KDF parameters in metadata.

3. Add hybrid fallback and negotiation
Why: During migration, you may need to support both RSA and PQC keys.
What to change

Implement a key version and algorithm identifier in the wrapped key blob.

On decrypt, inspect the identifier and route to the correct unwrap routine (RSA or KEM).

Provide a CLI migration command that rewraps existing DEKs with the new KEM while keeping an audit trail.

4. Harden the KMS design
Why: The current KMS is educational; production systems require stronger protections.
What to change

Protect master key: avoid storing the master key as a raw file; use an OS keystore or HSM for the master key in production.

Access controls: add role‑based access checks around key operations.

Audit: extend audit logs with operator identity, operation outcome, and request origin.

Secure deletion: when revoking keys, securely wipe any in‑memory copies and consider cryptographic shredding strategies for disk artifacts.

5. Improve testing and CI
Why: Tests ensure correctness across algorithm changes and migrations.
What to change

Add unit tests for KEM encapsulation/decapsulation, HKDF derivation, and Fernet round trips.

Add migration tests that simulate RSA→KEM rewraps.

Add CI that runs tests on multiple Python versions and with the PQC library installed.

6. Performance and size considerations
Why: PQC keys and ciphertexts can be larger and slower.
What to change

Benchmark encapsulation/decapsulation and encryption/decryption.

Consider caching derived symmetric keys for short‑lived sessions (with strict TTL).

Document tradeoffs in README.

7. Documentation and developer ergonomics
Why: Clear docs help reviewers and future you.
What to change

Add a Migration Guide describing how to move from RSA to KEM, including sample commands.

Add a Threat Model section describing attacker capabilities and assumptions.

Add inline comments in crypto code explaining parameter choices and KDF usage.

Repo Structure
Code
Hybrid-Crypto-KMS/
├─ README.md
├─ main.py
├─ KMS/
│  ├─ key_manager.py
│  ├─ keystore.enc
│  └─ metadata.json
├─ Hybrid_AES_RSA.py
├─ keys/
│  ├─ private.pem
│  └─ public.pem
Important Add KMS/master.key, keys/private.pem, and any PQC private key files to .gitignore to avoid committing sensitive material.

Tests and Validation
Include unit tests that cover:

Keystore save and load with the master key.

Storing and loading keys through the KMS API.

Rotation re‑encrypts the keystore without losing entries.

Revocation removes keys and updates metadata.

Encryption and decryption round trips using the hybrid flow.

Migration tests for RSA→KEM rewraps and backward compatibility.

Suggested test tools: pytest for unit tests and small fixtures to simulate keystore files.

Contributing
Open an issue for bugs or feature requests.

For code contributions, fork the repo, create a feature branch, and submit a pull request with a clear description of changes.

Keep changes small and focused so reviewers can follow the cryptographic intent.

License
This project is suitable for portfolio and educational use. A permissive license such as MIT is recommended.

Final Notes
This repository is meant to be a learning aid. It shows how envelope encryption and basic key management concepts work in practice. Use it to explore, experiment, and build understanding, and pair it with production grade tooling and reviews before using similar patterns for real secrets.

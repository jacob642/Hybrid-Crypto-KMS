# Hybrid-Crypto-KMS
This project is a practical implementation of hybrid encryption and key management in Python. It uses Fernet which provides AES 128 CBC with HMAC SHA256 for fast authenticated encryption and RSA OAEP to securely wrap the symmetric key. Alongside the crypto logic it includes a small Key Management System that stores keys in an encrypted keystore tracks metadata rotates master keys and supports key revocation.

I built this during my internship as a way to understand how secure systems actually manage keys behind the scenes. It helped me move beyond simple encryption examples and into the full lifecycle of key creation storage rotation and revocation.

What the Project Does
Hybrid Encryption
The encryption process works like this

A Fernet key is generated
The Fernet key is encrypted using RSA OAEP
The message is encrypted using the Fernet key
The Fernet key is stored securely in the KMS
Decryption reverses the process

This mirrors how many real systems combine symmetric and asymmetric encryption.

Key Management System
The KMS handles

Creating and storing a master key
Encrypting and saving keys in a keystore
Tracking metadata such as creation time last access and revocation
Rotating the master key
Revoking keys
Logging actions to an audit log

Sensitive files such as RSA keys the master key and logs are ignored through the gitignore file.

Project Structure
Code
Hybrid Crypto KMS
    Hybrid AES RSA.py        Hybrid encryption and decryption logic
    KMS.py                   Key management system
    main.py                  CLI runner
    keys                     RSA keys ignored
    KMS                      Keystore master key metadata audit log
    gitignore
    LICENSE
    README.md
How to Run
Install dependencies

pip install r requirements.txt

Run the main program

python main.py

The program will

Set up the KMS
Generate RSA keys if needed
Generate a Fernet key and store it
Encrypt your message
Decrypt it again
Rotate the master key
Ask whether you want to revoke the key

It is a simple flow but it covers the full lifecycle.

Internship Context
I built this during my internship to get hands on experience with hybrid encryption key storage and protection rotation and revocation audit logging and structuring a complete security tool. It helped me understand how secure systems behave beyond basic encryption examples.

Possible Improvements
There are several things I would improve if I continued working on this

Use stronger RSA keys such as 4096 bit
Improve separation of modules
Add better error handling with custom exceptions
Write unit tests for encryption decryption rotation and revocation
Allow configurable storage paths instead of fixed directories
Support multiple key types
Add optional post quantum support
Replace the simple input prompts with a proper command line interface

These changes would make the project more robust and closer to something used in production

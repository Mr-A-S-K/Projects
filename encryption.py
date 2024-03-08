from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path, key):
    cipher = Cipher(algorithms.AES(key), modes.CFB8(os.urandom(16)), backend=default_backend())

    with open(file_path, 'rb') as file:
        plaintext = file.read()

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(ciphertext)

    return encrypted_file_path

def decrypt_file(encrypted_file_path, key):
    cipher = Cipher(algorithms.AES(key), modes.CFB8(os.urandom(16)), backend=default_backend())

    with open(encrypted_file_path, 'rb') as encrypted_file:
        ciphertext = encrypted_file.read()

    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    decrypted_file_path = encrypted_file_path.replace('.encrypted', '_decrypted')
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(plaintext)

    return decrypted_file_path

file_path = r"C:/Users/adith/Downloads/coverletters/adithya.txt"
password = input("Enter encryption password: ")
salt = os.urandom(16)

key = generate_key(password, salt)

encrypted_file_path = encrypt_file(file_path, key)
print(f"File encrypted: {encrypted_file_path}")

decrypted_file_path = decrypt_file(encrypted_file_path, key)
print(f"File decrypted: {decrypted_file_path}")

# app.py

from flask import Flask, render_template, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

app = Flask(__name__)

# AES encryption function
def encrypt_message(key, plaintext):
    backend = default_backend()
    iv = os.urandom(16)  # generate a random IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode('utf-8')

# AES decryption function
def decrypt_message(key, ciphertext):
    backend = default_backend()
    decoded = base64.b64decode(ciphertext)
    iv = decoded[:16]
    ciphertext = decoded[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
    return decrypted_data.decode('utf-8')

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Encryption route
@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    plaintext = data['plaintext']
    key = b'Sixteen byte key'  # Replace with your own AES key (must be 16, 24, or 32 bytes long)
    ciphertext = encrypt_message(key, plaintext)
    return jsonify({'ciphertext': ciphertext})

# Decryption route
@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    ciphertext = data['ciphertext']
    key = b'Sixteen byte key'  # Replace with your own AES key (must be 16, 24, or 32 bytes long)
    plaintext = decrypt_message(key, ciphertext)
    return jsonify({'plaintext': plaintext})

if __name__ == '__main__':
    app.run(debug=True)

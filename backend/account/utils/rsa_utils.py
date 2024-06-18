from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

# Generate RSA keys
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

def encrypt_message(message, public_key):
    encrypted = public_key.encrypt(
        message.encode('utf-8'),  # Ensure the message is encoded as bytes
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    encrypted_base64 = base64.b64encode(encrypted).decode('utf-8')  # Base64 encode and convert to string
    return encrypted_base64

def decrypt_message(encrypted_message, private_key):
    try:
        message = encrypted_message.encode('utf-8')
        decoded_encrypted_message = base64.b64decode(message)
        decrypted = private_key.decrypt(
            decoded_encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting message: {e}")
        raise  # Re-raise the exception for debugging purposes

# Save the private key for later use
try:
    with open("private_key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
except Exception as e:
    print(f"Error saving private key: {e}")

# Save the public key for later use
try:
    with open("public_key.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
except Exception as e:
    print(f"Error saving public key: {e}")

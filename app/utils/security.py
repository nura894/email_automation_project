from passlib.context import CryptContext  #hashing algorithms
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

pwd_context= CryptContext(
    schemes=["argon2"],
    deprecated= "auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



#Encryption

load_dotenv()

key = os.getenv("ENCRYPTION_KEY").encode()
cipher = Fernet(key)


def encrypt_password(password: str) -> str:
    encrypted = cipher.encrypt(password.encode())
    return encrypted.decode()


def decrypt_password(encrypted_password: str) -> str:
    decrypted = cipher.decrypt(encrypted_password.encode())
    return decrypted.decode()

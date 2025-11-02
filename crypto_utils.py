import base64
import hashlib
from cryptography.fernet import Fernet

def derive_key_from_string(key_str: str) -> bytes:
    """
      Transforma uma string em uma chave válida (base64-encoded)
    """
    sha = hashlib.sha256(key_str.encode()).digest()
    return base64.urlsafe_b64encode(sha)

def encrypt_message(message: str, key_str: str) -> str:
    """
      Cifra a mensagem usando uma chave derivada da string fornecida.
      Retorna o token como string.
    """
    key = derive_key_from_string(key_str)
    f = Fernet(key)
    token = f.encrypt(message.encode())
    return token.decode()

def decrypt_message(token: str, key_str: str) -> str:
    """
      Decifra a mensagem cifrada usando a string de chave.
    """
    key = derive_key_from_string(key_str)
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()

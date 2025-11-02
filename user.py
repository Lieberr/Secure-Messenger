import bcrypt
from typing import Dict, Any, Optional
from db import DB

class User:
    def __init__(self, nickname: str, str_password: str, hashed_password: Optional[bytes] = None):

        self.nickname = nickname
        if hashed_password:
            self.password = hashed_password
        else:
            self.password = User.hash_password(str_password)


    # Metodos estaticos para hash e verificacao de senha

    @staticmethod
    def hash_password(password: str) -> bytes:
        # Gerar o hash da senha usando bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    @staticmethod
    def verify_password(password: str, hashed: bytes) -> bool:
        # Verificar se a senha corresponde ao hash armazenado
        return bcrypt.checkpw(password.encode("utf-8"), hashed)


    #Metodos de persistencia

    def to_dict(self) -> Dict[str, Any]:
        # Converter o objeto User para um dicionario para armazenamento no MongoDB
        return {
            "nickname": self.nickname,
            "password": self.password
        }
    
    def save(self) -> bool:
        #Salvar o usuario no banco de dados, se o nickname for unico
        if not DB.is_connected(): return False

        users_col = DB. get_users_collection()
        if users_col.find_one({"nickname": self.nickname}):
            print(f"✖️ Nickname '{self.nickname}' ja esta em uso.")
            return False
        
        users_col.insert_one(self.to_dict())
        return True
    

    @classmethod
    def find_by_nickname(cls, nickname: str) -> Optional['User']:
        #Buscar um usuario pelo nickname no DB
        if not DB.is_connected(): return None

        users_col = DB.get_users_collection()
        user_data = users_col.find_one({"nickname": nickname})

        if user_data:
            return cls(
                nickname=user_data["nickname"],
                str_password="",
                hashed_password=user_data["password"]
            )
        return None
    

    @classmethod
    def authenticate(cls, nickname: str, str_password: str) -> Optional['User']:
        #Autenticar um usuario
        user = cls.find_by_nickname(nickname)
        if user and cls.verify_password(str_password, user.password):
            return user
        return None
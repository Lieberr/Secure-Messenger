import bcrypt

class User:
    def __init__(self, nickname: str, str_password: str):
        self.nickname = nickname
        self.password = User.hash_password(str_password)

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    @staticmethod
    def verify_password(password: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed)

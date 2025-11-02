from user import User
from crypto_utils import encrypt_message, decrypt_message
from db import DB
from typing import Dict, Any, Optional, List
from datetime import datetime
from bson.objectid import ObjectId


class Message:
    def __init__(self, uFrom: User, uTo: User, encrypted_msg: str, status: str = "Nova", _id: Optional[ObjectId] = None, timestamp: Optional[datetime] = None):
        self.uFrom = uFrom
        self.uTo = uTo
        self.encrypted_msg = encrypted_msg
        self.status = status # "Nova" ou "Lida"
        self.timestamp = timestamp if timestamp else datetime.now()
        self._id = _id # ID do MongoDB


    #Metodos de persistencia

    def to_dict(self) -> Dict[str, Any]:
        #Converter o objeto message para um dicionario salvavel no mongoDB
        return {
            "from_nickame": self.uFrom.nickname,
            "to_nickname": self.uTo.nickname,
            "encrypted_msg": self.encrypted_msg,
            "status": self.status,
            "timestamp": self.timestamp
        }
    
    def save(self):
        #salvar a mensagem no banco de dados
        if not DB.is_connected(): return

        messages_col = DB.get_messages_collection()
        result = messages_col.insert_one(self.to_dict())
        self._id = result.inserted_id

    def decrypt_and_display(self, key_str: str) -> str:
        #Descriptografar a mensagem e retornar o texto
        try:
            decrypted = decrypt_message(self.encrypted_msg, key_str)

            if self.status == "Nova":
                self.mark_as_read()
            

            return decrypted
        except Exception:
            return "✖️ Erro ao descriptografar a mensagem. Verifique a chave."
        


    def mark_as_read(self):
        #Atualiza o status da mensagem no banco de dados para "lida"
        if not DB.is_connected(): return

        messages_col = DB.get_messages_collection()
        messages_col.update_one(
            {"_id": self._id},
            {"$set": {"status": "Lida"}}
        )

        self.status = "Lida"

    
    #Metodos de classe para buscar mensagens
    @classmethod
    def create_and_send(cls, uFrom: User, to_nickname: str, raw_msg: str, key_str: str) -> Optional['Message']:
        # Cria a mensagem, cifra e salva no bd
        uTo = User.find_by_nickname(to_nickname)
        if not uTo:
            print(f"✖️ Usuario com nickname '{to_nickname}' nao encontrado.")
            return None
        
        # 1. Cifrar a mensagem ANTES de criar o objeto
        encrypted = encrypt_message(raw_msg, key_str)

        #2. Criar o objeto mensagem
        new_message = cls(uFrom, uTo, encrypted)
        new_message.save()
        print(f"✅ Mensagem enviada para @{to_nickname} com sucesso. Status: '{new_message.status}'")
        return new_message
    

    @staticmethod
    def get_inbox_for_user(user: User) -> List['Message']:
        # Retorna todas as mensagens do inbox do usuario
        if not DB.is_connected(): return []

        messages_col = DB.get_messages_collection()
        message_dicts = messages_col.find(
            {"to_nickname": user.nickname}
          ).sort("timestamp", -1) # mais novas primeiro
        
        inbox = []
        for msg_data in message_dicts:
            uFrom = User.find_by_nickname(msg_data["from_nickame"])
            # uFrom pode ser None se o usuario for deletado

            message = Message(
                uFrom=uFrom or User("Desconhecido", ""), #Lida com remente nao encontrado
                uTo=user,
                encrypted_msg=msg_data["encrypted_msg"],
                status=msg_data["status"],
                _id=msg_data["_id"],
                timestamp=msg_data["timestamp"]
            )
            inbox.append(message)
        return inbox
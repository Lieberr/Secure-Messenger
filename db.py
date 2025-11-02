from pymongo import MongoClient
from typing import Dict, Any

# Configuracoes do MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "secure_messenger_db"

class Database:
    #Gerenciar a conexao com o banco de dados MongoDB

    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            
            #Tentar verificar a conexao
            self.client.admin.command('ping')
            self.db = self.client[DATABASE_NAME]
            self.users_collection = self.db["users"]
            self.messages_collection = self.db["messages"]
            print("✅ Conexao com o MongoDB estabelecida com sucesso.")

        except Exception as e:
            print(f"✖️ Erro ao conectar ao mongoDB. Verifique se o servidor esta rodando")
            print(f"Detalhes do erro: {e}")
            self.client = None
            self.db = None

    def is_connected(self) -> bool:
        return self.client is not None
    
    def close(self):
        # Fechar a conexao com o banco de dados
        if self.client:
            self.client.close()

    
    def get_users_collection(self):
        return self.users_collection
    
    def get_messages_collection(self):
        return self.messages_collection
    
#Instancia global do banco de dados
DB = Database()
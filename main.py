from user import User
from message import Message
from db import DB
import getpass
import sys
from typing import Dict, Any, Optional, List


CURRENT_USER: Optional[User] = None



def main_menu():
    global CURRENT_USER

    if not DB.is_connected():
        print("✖️ Nao e possivel conectar ao banco de dados. Encerrando o programa.")
        DB.close()
        sys.exit(1)

    while True:
        print("\n=== Secure Messenger - Menu Principal ===")
        if CURRENT_USER:
            print(f"Usuario logado: @{CURRENT_USER.nickname}")
            print("1. Enviar Mensagem Cifrada")
            print("2. Ler mensagens (caixa de entrada)")
            print("3. Logout")
            print("4. Sair")
            choice = input("Escolha uma opcao: ")

            if choice == "1":
                send_message()
            elif choice == "2":
                read_messages()
            elif choice == "3":
                CURRENT_USER = None
                print("✅ Logout realizado com sucesso.")
            elif choice == "4":
                break
            else:
                print("Opcao invalida. Tente novamente.")
        else:
            print("1. Login")
            print("2. Registrar Novo Usuario")
            print("3. Sair")
            choice = input("Escolha uma opcao: ")

            if choice == "1":
                login()
            elif choice == "2":
                register_user()
            elif choice == "3":
                break
            else:
                print("Opcao invalida. Tente novamente.")
    DB.close()
    print("Encerrando o Secure Messenger. Ate logo!")
    sys.exit(0)


def register_user():
    # Registrar novo usuario
    nickname = input("Digite o nickname desejado: ").strip()
    if not nickname:
        print("✖️ Nickname nao pode ser vazio.")
        return
    
    # User getpass para esconder a senha
    password = getpass.getpass("Digite a senha desejada: ")

    new_user = User(nickname, password)
    if new_user.save():
        print(f"✅ Usuario '@{nickname}' registrado com sucesso.")

def login():
    # AUtenticar usuario existente
    global CURRENT_USER
    nickname = input("Nickname (@): ").strip()
    password = getpass.getpass("Senha: ")

    user = User.authenticate(nickname, password)
    if user:
        CURRENT_USER = user
        print(f"✅ Login bem-sucedido. Bem-vindo, @{nickname}!")
    else:
        print("✖️ Falha no login. Verifique seu nickname e senha.")

def send_message():
    # Enviar mensagem cifrada
    if not CURRENT_USER: return

    to_nickname = input("Enviar para @: ").strip()
    key_str = input("Chave Compartilhada (texto p/ Cifragem): ").strip()
    raw_msg = input("Digite a mensagem: ").strip()

    if not to_nickname or not key_str or not raw_msg:
        print("✖️ Todos os campos sao obrigatorios.")
        return
    
    Message.create_and_send(CURRENT_USER, to_nickname, raw_msg, key_str)


def read_messages():
    # Exibe as mensagens e permite a decifragem local
    if not CURRENT_USER: return

    inbox = Message.get_inbox_for_user(CURRENT_USER)

    if not inbox:
        print("Sua caixa de entrada esta vazia.")
        return

    print(f"\n=== Caixa de Entrada de @{CURRENT_USER.nickname} ===")
    print(f"{'#':<3} | {'De':<15} | {'Status':<6} | {'Data':<16}")
    print("-" * 50)

    for i, msg in enumerate(inbox):
        date_str = msg.timestamp.strftime("%Y-%m-%d %H:%M")
        print(f"{i:<3} | {msg.uFrom.nickname:<15} | {msg.status:<6} | {date_str:<16}")

    print("-" * 50)

    try:
        msg_input = input("Digite o numero da mensagem para ler (ou 's' para voltar): ")
        if msg_input.lower() == 's':
            return
        
        msg_index = int(msg_input)
        if 0 <= msg_index < len(inbox):
            message_to_read = inbox[msg_index]



        while True:
            print(f"\n--- Decifrar Mensagem de @{message_to_read.uFrom.nickname} ---")
            key_str = input("Digite a CHAVE COMPARTILHADA (ou 'c' para cancelar): ")
            
            if key_str.lower() == 'c':
                print("decifragem cancelada.")
                break


            #Tentar decifrar
            decrypted_text = message_to_read.decrypt_and_display(key_str)

            print("\n--- 🔓 Resultado da Decifragem ---")
            print(f"Status: {message_to_read.status}")
            print(f"Mensagem: {decrypted_text}")
            print("-----------------------------------")

            if decrypted_text.startswith("✖️"):
                print("Tente novamente com a chave correta.")
            else:
                # se decifrou com sucesso, sair do loop
                break


        else:
            print("✖️ Indice de mensagem invalido.")

    except ValueError:
        print("✖️ Entrada invalida. Por favor, digite um numero valido.")

if __name__ == "__main__":
    main_menu()
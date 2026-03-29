# 🔒 Secure Messenger – Projeto de Mensagens Criptografadas

Um mensageiro simples em **Python**, utilizando **MongoDB** como banco de dados e **criptografia simétrica** com chave compartilhada entre os usuários.
As mensagens **são cifradas** antes de serem armazenadas e só podem ser acessadas **(decifradas)** pelo destinatário que possui a chave correta, garantindo confidencialidade das informações.

---

## 📌 Funcionalidades

- Registro e autenticação de usuários (com senha criptografada via *bcrypt*)
- Envio de mensagens cifradas com uma **chave textual compartilhada**
- Armazenamento seguro das mensagens no **MongoDB**
- Mensagens têm status `"Nova"` e `"Lida"`
- Decifragem apenas local (nunca no transporte ou no banco)
- Erro controlado caso a chave informada esteja incorreta

---

## 🔒 Segurança

- Criptografia sim~etrica para proteção de mensagens
- Senhas armazenadas com hash seguro (bycrpt)
- Dados sens~iveis nunca armazenados em texto puro
- Descriptografia realizada apenas localmente (Não no banco de dados ou transporte)

---

## 🛠️ Tecnologias

- Python
- MongoDB
- PyMongo
- Cryptography
- Bcrypt
- Git & GitHub

---

## 🧠 Como Funciona

1. O usuário envia uma mensagem utilizando uma chave compartilhada  
2. A mensagem é criptografada antes de ser armazenada no banco  
3. O destinatário acessa a mensagem e informa a chave  
4. A descriptografia ocorre localmente, exibindo o conteúdo original  

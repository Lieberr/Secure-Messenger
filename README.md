# Secure Messenger – Projeto de Mensagens Criptografadas

Um mensageiro simples em **Python**, utilizando **MongoDB** como banco de dados e **criptografia simétrica** com chave compartilhada entre os usuários.
As mensagens são **cifradas antes de serem armazenadas** e **só são decifradas na interface do destinatário** com a chave correta.

---

## Funcionalidades

* Registro e autenticação de usuários (com senha criptografada via *bcrypt*)
* Envio de mensagens cifradas com uma **chave textual compartilhada**
* Armazenamento seguro das mensagens no **MongoDB**
* Mensagens têm status `"Nova"` e `"Lida"`
* Decifragem apenas local (nunca no transporte ou no banco)
* Erro controlado caso a chave informada esteja incorreta

---

## Exemplo de uso

```
Usuário Bob entra e envia para @Alice
→ Chave compartilhada: "puc"
→ Mensagem: "Oi Alice!"

Alice faz login, vai em "Ler mensagens"
→ Digita chave: "puc"
→ Mensagem decifrada com sucesso.
```

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from encryption import encrypt_message, decrypt_message

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    while True:
        try:
            encrypted_message = client.recv(BUFSIZ)
            message = decrypt_message(encrypted_message)
            broadcast(message, client)
        except OSError:
            client.close()
            break

def broadcast(message, client_socket):
    encrypted_message = encrypt_message(message)
    for client in clients:
        if client != client_socket:
            client.send(encrypted_message)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

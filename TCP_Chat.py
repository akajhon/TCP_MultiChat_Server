import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 134

# Starting Server
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((SERVER_HOST, SERVER_PORT))
SERVER.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)
        
 
# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            msg = message = client.recv(1024)
            
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'ADMIN':
                    kicked = msg.decode('ascii')[5:]
                    kick_user(kicked)
                else:
                    client.send('Não é ADMIN'.encode('ascii'))
                    
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'ADMIN':
                    banned = msg.decode('ascii')[4:]
                    kick_user(banned)
                    with open('bans.txt', 'a') as f:
                        f.write(f'{banned}\n')
                    print(f'{banned} Foi Banido do chat!!')
                else:
                    client.send('Não é ADMIN'.encode('ascii'))
            else:
                broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} Saiu do Chat!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        
        with open('bans.txt', 'r') as f:
            bans = f.readlines()
            
        if nickname+'\n' in bans:
            client.send('BANNED'.encode('ascii'))
            client.close()
            continue
        
        if nickname == 'ADMIN':
            client.send('Senha:'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != '1234':
                client.send('Wrong Password'.encode('ascii'))
                client.close()
                continue
            
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} Entrou no chat!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('Você foi banido'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} foi kickado'.encode('ascii'))

receive()
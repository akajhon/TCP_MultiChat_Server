from datetime import datetime
from pyfiglet import Figlet
from colorama import Fore, Style
import threading
import socket
import os
import sys
import hashlib

PORT = 8000
width = os.get_terminal_size().columns
pos = round(width/2)
users = dict()
nicknames = list()
rooms = {"Lobby": [], "Room01": []}
ADMIN_HASHED_PASSWD = hashlib.sha256('adminpassword'.encode('utf-8')).hexdigest()

instructions = b'-------------------------------------------------------' \
				+ b'\n[+] Comandos Validos [+]\n'\
				+ b'[/CREATE] Para criar uma sala\n'\
				+ b'[/JOIN] Para entrar em uma sala\n' \
                + b'[/LIST] Para listar as salas disponiveis\n' \
                + b'[/LISTUSERS] Para listar os usuarios conectados\n' \
                + b'[/LISTBANNED] Para listar os usuarios banidos\n' \
                + b'[/DELETE] Para deletar uma sala\n'\
                + b'[/TIME] Para mostrar o horario atual\n' \
                + b'[/BAN]  Para banir um usuario\n' \
                + b'[/UNBAN] Para desbanir um usuario do servidor\n' \
				+ b'[/LEAVE] Para sair da sala\n' \
				+ b'[/EXIT] Para encerrar a conexao com o servidor\n' \
				+ b'[/KICK] Para kickar um usuario da sala\n' \
                + b'[/HELP] Para exibir a lista de comandos disponiveis\n' \
				+ b'-------------------------------------------------------' \
				+ b'\n'

def help(client):
    client.sendall(instructions)

def list_rooms(client):
    response = "\n[+] Salas disponíveis:\n"
    for room, room_clients in rooms.items():
        response += f"[+]{room} : {len(room_clients)} Usuários\n"
    client.sendall(response.encode('utf-8'))

def list_users(client):
    if len(nicknames) != 0 :
        response = "\n[+] Usuários Conectados:\n"
        for nicks in nicknames:
            response += f"[+] {nicks} "
            response += "\n"
        client.sendall(response.encode('utf-8'))
    else:
        response = "[!] Não existem usuários conectados[!]\n"
        client.sendall((Fore.RED + response + Style.RESET_ALL).encode("utf-8"))

def list_banned_users(client):
    with open('bans.txt', 'r') as f:
        data = f.readlines()
        f.close()
        banned_users = [line.strip("\n") for line in data]
        if len(banned_users) == 0:
            response = "[!] Não existem usuários Banidos [!]\n"
            client.sendall((Fore.RED + response + Style.RESET_ALL).encode("utf-8"))
        else:
            banned_user_list = "\n[+] Lista de usuarios Banidos [+]\n"
            for users in banned_users:
                banned_user_list += f"[+] {users}"
                banned_user_list += "\n"
            client.sendall(banned_user_list.encode('utf-8'))       

def join(client):
    client.sendall("\n[+] Salas disponíveis:\n".encode('utf-8'))
    for keys in rooms:
        client.sendall(f"-> {keys}\n".encode('utf-8'))
    client.sendall("[+] Deseja entrar em qual sala: ".encode('utf-8'))
    room_name = client.recv(1024).decode('utf-8')
    room_name = room_name.replace("\n", "").replace("\r", "")
    try:
        origin_room = find_client_room(client)
        rooms[room_name].append(client)
        rooms[origin_room].remove(client)
        client.sendall((Fore.GREEN + f"[!] Bem vindo a sala {room_name} [!]\n" + Style.RESET_ALL).encode('utf-8'))
    except:
        response = "[!] Essa sala não existe no servidor [!]\n"
        client.sendall((Fore.RED + response + Style.RESET_ALL).encode('utf-8'))

def leave(client):
    try:
        client.sendall("[+] Tem certeza que deseja sair da sala? (sim/nao) ".encode('utf-8'))
        answer = client.recv(1024).decode('utf-8')
        answer = answer.replace("\n", "").replace("\r", "")
        if answer.lower() == 'sim':
            origin_room = find_client_room(client)
            rooms["Lobby"].append(client)
            rooms[origin_room].remove(client)
            client.sendall(f"[+] Você saiu da sala {origin_room} e está no Lobby!\n".encode('utf-8'))
        else:
            pass
    except:
        response = "[!] Erro ao sair da sala [!]\n"
        client.sendall((Fore.RED + response + Style.RESET_ALL).encode("utf-8"))

def create_room(client):
    origin_room = find_client_room(client)
    client.sendall("[+] Entre com o nome da sala que deseja criar: ".encode('utf-8'))
    room_name = client.recv(1024).decode('utf-8')
    room_name = room_name.replace("\r", "").replace("\n", "")
    rooms[room_name] = [client]
    rooms[origin_room].remove(client)
    join(client)
    print(Fore.GREEN + (f"[!] Sala {room_name} criada [!]\n") + Style.RESET_ALL)

def delete_room(client):
    try:
        client.sendall("[+] Entre com o nome da sala que deseja excluir: ".encode('utf-8'))
        room_name = client.recv(1024).decode('utf-8')
        room_name = room_name.replace("\r", "").replace("\n", "")
        room_clients = rooms[room_name]
        rooms["Lobby"].append(room_clients)
        rooms.pop(room_name)
        client.sendall((Fore.RED + (f"[!] Sala {room_name} deletada [!]\n") + Style.RESET_ALL).encode('utf-8'))
        print(Fore.RED + (f"[!] Sala {room_name} deletada [!]\n") + Style.RESET_ALL)
    except Exception as e:
        client.sendall((Fore.RED + (f"[!] Erro ao deletar a sala {room_name} [!]\n") + Style.RESET_ALL).encode('utf-8'))
        print(Fore.RED + (f"[!] Erro {e} ao deletar a sala {room_name} [!]\n") + Style.RESET_ALL)

def find_client_room(client):
    for room, room_clients in rooms.items():
        if client in room_clients:
            return room

def find_nickname_client(client):
    user_nickname = users[client]['nickname']
    return user_nickname

def find_client_nickname(nickname):
    for con, user in users.items():
        for keys in user.items():
            if nickname in keys:
                user_client = con
    return user_client

def check_password(client, passwd):
    passwd.encode('utf-8')
    hashed_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    if hashed_passwd == users[client]['password'] or hashed_passwd == ADMIN_HASHED_PASSWD:
        return True
    else:
        return False

def ban_user(client):
    while True:
        client.sendall("[+] Digite a senha de ADMIN: ".encode('utf-8'))
        psswd = client.recv(1024).decode('utf-8')
        psswd = psswd.replace("\n", "").replace("\r", "")
        checked_psswd = check_password(client, psswd)
        if checked_psswd == True:
            client.sendall("[+] Digite o nome do usuário que será banido: ".encode('utf-8'))
            user = client.recv(1024).decode('utf-8')
            user = user.replace("\n", "").replace("\r", "")
            with open('bans.txt', 'a') as f:
                f.write(f'{user}\n')
                f.close()
            client.sendall((Fore.RED + f'[!] O usuário {user} foi banido do chat [!]\n' + Style.RESET_ALL).encode('utf-8'))
            print(Fore.RED + f'[!] O usuário {user} foi banido do chat [!]\n' + Style.RESET_ALL)
            break
        else:
            client.sendall((Fore.RED + "[!] Senha incorreta [!]\n" + Style.RESET_ALL).encode('utf-8'))
            continue

def unban_user(client):
    while True:
        client.sendall("[+] Digite a senha de ADMIN: ".encode('utf-8'))
        psswd = client.recv(1024).decode('utf-8')
        psswd = psswd.replace("\n", "").replace("\r", "")
        checked_psswd = check_password(client, psswd)
        if checked_psswd == True:
            client.sendall("[+] Digite o nome do usuário que será desbanido: ".encode('utf-8'))
            user = client.recv(1024).decode('utf-8')
            user = user.replace("\n", "").replace("\r", "")
            with open("bans.txt", "r+") as f:
                data = f.readlines()
                f.truncate(0)
                f.close()
                wr_name = False
                with open("bans.txt", "w") as f:
                    for line in data :
                        if line == user+"\n":
                            wr_name = True
                            try:
                                data.remove(line)
                                for names in data:
                                    f.write(names)
                                f.close()
                            except Exception as e:
                                client.sendall((Fore.RED + f"[!] Erro ao gravar no arquivo [!]\n" + Style.RESET_ALL).encode('utf-8'))
                                print(Fore.RED + (f"[!] Erro {e} ao gravar no arquivo [!]\n") + Style.RESET_ALL)
                    if wr_name == False :
                        client.sendall((Fore.GREEN + f"[!] Usuário {user} não está na lista de banimento [!]\n" + Style.RESET_ALL).encode('utf-8'))
                        break
                client.sendall((Fore.GREEN + f"[!] Usuário {user} foi desbanido do chat [!]\n" + Style.RESET_ALL).encode('utf-8'))
                print(Fore.GREEN + (f"[!] O Usuário {user} foi Desbanido do servidor [!]\n") + Style.RESET_ALL)
                break
        else:
            client.sendall((Fore.RED + "[!] Senha incorreta [!]\n" + Style.RESET_ALL).encode('utf-8'))
            continue

def kick_user(client):
    while True:
        client.sendall("[+] Digite a senha de ADMIN: ".encode('utf-8'))
        psswd = client.recv(1024).decode('utf-8')
        psswd = psswd.replace("\n", "").replace("\r", "")
        checked_psswd = check_password(client, psswd)
        if checked_psswd == True:
            client.sendall("[+] Digite o nick do usuario que sera kickado:".encode('utf-8'))
            kick_user = client.recv(2046).decode('utf-8')
            kick_user = kick_user.replace("\n", "").replace("\r", "")
            user_con = find_client_nickname(kick_user)
            origin_room = find_client_room(user_con)
            rooms["Lobby"].append(user_con)
            rooms[origin_room].remove(user_con)
            client.sendall((Fore.RED + f"[!] Usuário {kick_user} foi Kickado da sala {origin_room} [!]\n" + Style.RESET_ALL).encode('utf-8'))
            user_con.sendall((Fore.RED + f"[!] Você foi Kickado da sala {origin_room} [!]\n"+ Style.RESET_ALL).encode('utf-8'))
            print(Fore.RED + (f"[!] O Usuário {kick_user} foi kickado da sala {origin_room} [!]\n") + Style.RESET_ALL)
            break
        else:
            client.sendall((Fore.RED + "[!] Senha incorreta [!]\n" + Style.RESET_ALL).encode('utf-8'))
            continue

def time(client):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    client.sendall((Fore.BLUE + "[!] Always on time... [!]\n" + Style.RESET_ALL).encode('utf-8'))
    client.sendall(f"[+] Horario atual: {current_time}\n".encode('utf-8'))

def server_exit(client):
    client.sendall("[+] Tem certeza que deseja sair do servidor? (sim/nao) ".encode('utf-8'))
    answer = client.recv(1024).decode('utf-8')
    answer = answer.replace("\n", "").replace("\r", "")
    if answer.lower() == 'sim':
        while True:
            client.sendall("[+] Digite sua senha: ".encode('utf-8'))
            psswd = client.recv(1024).decode('utf-8')
            psswd = psswd.replace("\n", "").replace("\r", "")
            checked_psswd = check_password(client, psswd)
            if checked_psswd == True:
                client.sendall((Fore.RED + (f"[!] Até logo... [!]\n") + Style.RESET_ALL).encode('utf-8'))
                nick = find_nickname_client(client)
                nicknames.remove(nick)
                origin_room = find_client_room(client)
                rooms["Lobby"].append(client)
                rooms[origin_room].remove(client)
                rooms["Lobby"].remove(client)
                del users[client]
                client.shutdown(1)
                client.close()
                print(Fore.RED + (f"[!] O Usuário {nick} escolheu sair do servidor [!]") + Style.RESET_ALL)
                break
            else:
                client.sendall((Fore.RED + "[!] Senha incorreta [!]\n" + Style.RESET_ALL).encode('utf-8'))
                continue
    else:
        client.sendall((Fore.GREEN + "[!] Otima escolha.... digite /help para exibir as opções [!]\n" + Style.RESET_ALL).encode('utf-8'))
        pass

def unique_nickname(nickname, client):
    while nickname in nicknames:
        client.sendall((Fore.RED + "[+] Este Nickname já está em uso...\n"+ Style.RESET_ALL).encode('utf-8'))
        client.sendall("[+] Nickname: ".encode('utf-8'))
        received = client.recv(1024).decode('utf-8')
        nickname = received.replace("\n", "").replace("\r", "")
    return nickname

COMMANDS = [
    {
        "action": "/list",
        "function": list_rooms,
    },
    {
        "action": "/listusers",
        "function": list_users,
    },
    {
        "action": "/listbanned",
        "function": list_banned_users,
    },
    {
        "action": "/help",
        "function": help,
    },
    {
        "action": "/join",
        "function": join,
    },
    {
        "action": "/leave",
        "function": leave,
    },
    {
        "action": "/create",
        "function": create_room,
    },
    {
        "action": "/delete",
        "function": delete_room,
    },
    {
        "action": "/time",
        "function": time,
    },
    {
        "action": "/exit",
        "function": server_exit,
    },
    {
        "action": "/ban",
        "function": ban_user,
    },
    {
        "action": "/kick",
        "function": kick_user,
    },
    {
        "action": "/unban",
        "function": unban_user,
    }, 
]

def is_valid_command(msg, client):
    aux = 0
    if msg.startswith("/") == True:
        command = str(msg).lower()
        for cmd in COMMANDS:
            if command == cmd["action"]:
                cmd["function"](client)
                return True
            elif aux == len(COMMANDS) and command != cmd["action"]:
                client.sendall(("[!] Comando inválido [!]\n").encode('utf-8'))
                return False
            else:
                pass
            aux+=1
        return False
    else:
        return False

def main():
    figlet = Figlet(font='doom', justify='center', width=width)
    banner = figlet.renderText("TCP CHAT SERVER")
    print(Fore.RED + banner + Style.RESET_ALL)
    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(Fore.GREEN + "[+] Socket criado com sucesso!! [+]" + Style.RESET_ALL)
    except socket.error as err:
        print(Fore.RED + "[+] Erro ao criar o socket... [+]" + Style.RESET_ALL,err)
        sys.exit()
    try:
        server.bind(("127.0.0.1",PORT))
        print(Fore.GREEN + f"[+] Servidor atrelado a porta {PORT} [+] " + Style.RESET_ALL)
    except:
        print(Fore.RED + "[!] Erro ao atrelar o servidor a porta... [!]" + Style.RESET_ALL)
        server.close()
        sys.exit()

    server.listen(100)
    print(Fore.GREEN + "[+] Servidor aguardando novas conexões... [+]\n" + Style.RESET_ALL)
    print((Fore.GREEN + "[+] A senha de administrador é: " + Style.RESET_ALL) + (Fore.RED + "adminpassword" + Style.RESET_ALL))

    while True:
        client, addr = server.accept()
        print(Fore.GREEN + (f"[+] Conexão realizada com o endereço {addr} [+]\n") + Style.RESET_ALL)
        figlet = Figlet(font='doom', justify='center', width=80)
        banner_client = figlet.renderText("TCP CHAT SERVER")
        client.sendall(banner_client.encode('ascii'))
        client.sendall("[+] Nickname: ".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nickname = nickname.replace("\n", "").replace("\r", "")
        nickname = unique_nickname(nickname, client)
        
        
        client.sendall("[+] Nome Completo: ".encode('utf-8'))
        full_name = client.recv(1024).decode('utf-8')
        full_name = full_name.replace("\n", "").replace("\r", "")

        client.sendall("[+] Senha: ".encode('utf-8'))
        passwd = client.recv(1024).decode('utf-8')
        passwd = passwd.replace("\n", "").replace("\r", "")
        hash_passwd  = hashlib.sha256(passwd.encode('utf-8')).hexdigest()   

        with open('bans.txt', 'r') as f:
            bans = f.readlines()

        if nickname+"\n" in bans:
            client.send('[!] Você foi banido do servidor [!]\n'.encode('utf-8'))
            client.close()
            print(Fore.RED + (f"[!] O Usuário {nickname} foi Banido e tentou se conectar [!]\n") + Style.RESET_ALL)
        else:
            nicknames.append(nickname)
            rooms["Lobby"].append(client)
            user = {} 
            user["nickname"] = nickname
            user["con"] = client
            user["full_name"] = full_name
            user["password"] = hash_passwd
            users[client] = user
            help(client)
            print(Fore.GREEN + (f"[+] Usuário {full_name} com o Nickname {nickname} conectado ao servidor [!]\n") + Style.RESET_ALL)
        
        thread = threading.Thread(target=messages_treatment, args=[client])
        thread.start()

def messages_treatment(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            msg = msg.replace("\n", "").replace("\r", "")
            try:
                has_command = is_valid_command(str(msg), client)
                if has_command == False:
                    broadcast(msg, client)
            except:
                delete_client(client)
                break
        except UnicodeDecodeError:
            client.sendall((Fore.RED + (f"[!] Até logo... [!]\n") + Style.RESET_ALL).encode('utf-8'))
            nick = find_nickname_client(client)
            nicknames.remove(nick)
            delete_client(client)
            del users[client]
            client.shutdown(1)
            client.close()
            print(Fore.RED + (f"[!] Usuário {nick} foi Desconectado por CTRL + C [!]\n") + Style.RESET_ALL)
            break
        except BaseException as e:
            pass
        

def broadcast(msg, client):
    user = find_nickname_client(client)
    msg_true = ("@"+str(user) + msg.rjust(pos) + '\n\r')
    for room_clients in rooms.values():
        if client in room_clients:
            for clientItem in room_clients:
                if clientItem != client:
                    try:
                        clientItem.send((Fore.GREEN + msg_true+ Style.RESET_ALL + '>').encode('utf-8'))
                    except:
                        print(Fore.RED + (f"[!] Erro ao realizar o Broadcast da mensagem [!]\n") + Style.RESET_ALL)
                        delete_client(clientItem)
            break

def delete_client(client):
    for room_clients in rooms.values():
        if client in room_clients:
            room_clients.remove(client)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + (f"[!] Servidor Encerrado [!]") + Style.RESET_ALL)
        print(Fore.RED + (f"[!] Até logo... [!]") + Style.RESET_ALL)
        sys.exit()

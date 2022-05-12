import socket 
import threading
import sys
import pickle



PORT = 1234
connections = dict()
number_of_chatrooms = 0
current_chatrooms = dict()
information = dict()

try:
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print("Socket is created successfully..")
except socket.error as err:
	print("Socket cannot be created...",err)
	sys.exit()

try:
	server.bind(("127.0.0.1",PORT))
	print("Server is binded successfully to port",PORT)
except:
	print("Server binding failed")
	server.close()
	sys.exit()

server.listen(100)
print("Server has started listening ..........")


def unique_nickname(nickname):
	''' Checks whether nickname is available or not'''

	while nickname in connections.keys():
		con.sendall("Notavailable".encode('utf-8'))
		nickname = con.recv(1024).decode('utf-8')
	
	return nickname


def store_messages(msg, room_name):
	# current_chatrooms[room_name]['messages'].append(msg)
	
	information[room_name]['messages'].append(msg)
	

	with open("messages.pickle","wb") as f:
		pickle.dump(information,f)

def broadcast_message(msg, nickname,con,room_name):
	''' sendalls message to everyone in chatroom '''

	msg = nickname +' : '+ msg.decode('utf-8')
	store_messages(msg,room_name)
	user_list = current_chatrooms[room_name]['users']
	for connection in user_list:
		if connection != nickname:
			user_list[connection].sendall(msg.encode('utf-8'))


def client_thread(nickname,con, name):
	''' Main client Thread which recieves message from client and broadcast to other clients'''

	user_list = current_chatrooms[name]['users']
	room_name = name
	while True:
		try:
			message = con.recv(1024).decode('utf-8')
			broadcast_message(message,nickname,con, name)
			print(message)
			if message.startswith('/quit'):
				del current_chatrooms[name]['users'][nickname]
				broadcast_message(f"{nickname} has left chatroom !!!".encode('utf-8'),nickname,con, connections)
				con.close()
				break
		except:
			#del current_chatrooms[name]['users'][nickname]
			#broadcast_message(f"{nickname} has left chatroom !!!".encode('utf-8'),nickname,con, connections)
			#con.close()
			break
def join_chatrooms(con, nickname, room_name):
	print("in join function")
	users = current_chatrooms[room_name]['users']
	users[nickname] = con
	current_chatrooms[room_name]['users'] = users

	information[room_name] = dict()
	information[room_name]['name'] = room_name
	information[room_name]['created_by'] = current_chatrooms[room_name]['created_by']
	information[room_name]['users'] = list(current_chatrooms[room_name]['users'].keys())
	information[room_name]['messages'] = []
	broadcast_message(f"{nickname} has joined the chatroom".encode('utf-8'),nickname,con,name)
	# con.sendall("Connected to server!".encode('utf-8'))
	con.sendall("Welcome to the chatroom !\n".encode('utf-8'))
	t = threading.Thread(target = client_thread, args = (nickname,con,name)).start()
	users = information[room_name]['users'] = list(current_chatrooms[room_name]['users'])
	print("Detalhes da sala: ",users)

def quit_chatroom(con, nickname, room_name):
	print("in join function")
	del current_chatrooms[room_name]['users'][nickname]
	#broadcast_message(f"{nickname} has left chatroom !!!".encode('utf-8'),nickname,con, connections)
	#con.close()
	


def create_chatroom(con,nickname,room_name):
	room_detail = dict()
	room_detail["name"] = room_name
	room_detail['users'] = dict()
	room_detail['created_by'] = nickname
	# room_detail['messages'] = []
	current_chatrooms[room_name] = room_detail

	print("room_detail",room_detail['users'])

	con.sendall(f"{name} created successfuly..".encode('utf-8'))



while True:
	con, addr = server.accept()
	print("Connection established with address \n",addr)
	con.sendall("Nickname: ".encode('utf-8'))
	nickname = con.recv(1024).decode('utf-8')
	nickname2 = nickname.replace("\r","")
	with open('bans.txt', 'r') as f:
		bans = f.readlines()
	if nickname2 in bans:
		con.send('[+] BANNED [+]\n'.encode('utf-8'))
		con.close()
		continue
	else: 
		nickname = unique_nickname(nickname)
		connections[nickname] = con
		con.sendall("enter NEW to Create chatroom or ENTER to join chatroom \n".encode('utf-8'))
		response = con.recv(1024).decode('utf-8')
		response1 = response.replace("\n", "")
		response2 = response1.replace("\r","")

		if response2 == 'new':
			con.sendall("Enter room name for your new chatrooms: \n".encode('utf-8'))
			name = con.recv(1024).decode('utf-8')
			# room = threading.Thread(target = create_chatroom, args = (con, nickname,name)).start()
			create_chatroom(con,nickname,name)
			# current_chatrooms['name'] = name
			number_of_chatrooms += 1
			con.sendall("Availabel chatrooms: \n".encode('utf-8'))
			for keys in current_chatrooms:
				con.sendall(f"{keys}\n".encode('utf-8'))
			con.sendall("Enter name of chatroom to join: \n".encode('utf-8'))
			answer = con.recv(1024).decode('utf-8')
			join_chatrooms(con,nickname,answer)

		elif response2 == 'enter':
			con.sendall("Availabel chatrooms: \n".encode('utf-8'))
			for keys in current_chatrooms:
				con.sendall(f"{keys}\n".encode('utf-8'))
			con.sendall("Enter name of chatroom to join: \n".encode('utf-8'))
			answer = con.recv(1024).decode('utf-8')
			join_chatrooms(con,nickname,answer)
		
		elif response2 == 'exit':
			con.close()

		elif response2 == 'ban':
			con.sendall("name: \n".encode('utf-8'))
			answer = con.recv(1024).decode('utf-8')
			with open('bans.txt', 'a') as f:
				f.write(f'{answer}\n')
			print(f'{answer} Foi Banido do chat!!')
			
		elif response2 == 'quit':
			con.sendall("Enter name of chatroom to quit: \n".encode('utf-8'))
			answer = con.recv(1024).decode('utf-8')
			con.sendall("Enter nickname: \n".encode('utf-8'))
			nickname = con.recv(1024).decode('utf-8')
			quit_chatroom(con,nickname,answer)
			
			# con.sendall("Availabel chatrooms: \n".encode('utf-8'))
			# for keys in current_chatrooms:
			# 	con.sendall(keys.encode('utf-8'))
			# con.sendall("Enter name of chatroom to join: \n".encode('utf-8'))
			# answer = con.recv(1024).decode('utf-8')
			# join_chatrooms(con,nickname,answer)

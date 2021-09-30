# from os import name
import socket
import threading
import psycopg2
import select
import json
import os
import time


# A list to hold names of users those are online
onlineClients = list()

# A list containing thread ids of each connection thread
applicationThread = list()

# Database connector
dbConn = psycopg2.connect(database="", user="postgres", password="12345678", host="localhost", port=5432)
dbConn.autocommit = True
dbCursor = dbConn.cursor()

# Creates a table that holds each registered user's credentials
try:	
	dbCursor.execute('''CREATE TABLE USERDATA (
		mobNo text PRIMARY KEY,
		name text);''')
	dbConn.commit()
except:
	print("Error in Creation of Table 'Userdata' or It already exists.") 

dbConn.close()

# To hndle the login process
def log_in(clientIdentifier, trialCounter, dbCursor, unreadMsgs, unreadChats):
	clientIdentifier.send("Enter your username: ".encode())
	username = str(clientIdentifier.recv(1024).decode()).strip()
	clientIdentifier.send("Enter your password: ".encode())
	password = str(clientIdentifier.recv(1024).decode()).strip()

	# trialcounter keeps the track of attempts made to login...
	# MAX attemps allowed = 3
	trialCounter -= 1

	dbCursor.execute("SELECT password from USERDATA where username='{}'".format(username))
	passwordList = dbCursor.fetchall()

	# passwordList contains password of user that is stored in DB IF IT EXISTS!!!
	# If length is greater than 0 that means user exists and then the password is matched
	if len(passwordList) > 0 and passwordList[0][0] == password:
		clientIdentifier.send("Log in successfull!!!".encode())
		onlineClients.append(username)
		dbCursor.execute('''SELECT COUNT(DISTINCT sender), COUNT(sender) from {} 
		where readreciept = 0;'''.format(username))
		readReport = dbCursor.fetchall()
		clientIdentifier.send('''You have {} unread messages from {} chats.'''.format(readReport[0][1], readReport[0][0]).encode())
		unreadMsgs = int(readReport[0][1])
		unreadChats = int(readReport[0][0])

	elif trialCounter >= 0:
		clientIdentifier.send("Invalid credentials!!!\nAttempts left: {}\n".format(trialCounter).encode())
		username = log_in(clientIdentifier, trialCounter, dbCursor, unreadMsgs, unreadChats)
	else:
		clientIdentifier.send("No attempts left try again after sometime!!!".encode())
		return False
	return username

# To carry out the process of signing in
def sign_in(clientIdentifier, dbConn):
	dbCursor = dbConn.cursor()
	clientIdentifier.send("Please write your first name: ".encode())
	name = str(clientIdentifier.recv(1024).decode()).strip()
	clientIdentifier.send("Please write your surname: ".encode())
	surname = str(clientIdentifier.recv(1024).decode()).strip()
	clientIdentifier.send("Please write a username for yourself: ".encode())
	username = str(clientIdentifier.recv(1024).decode()).strip()
	dbCursor.execute("SELECT COUNT(username) from USERDATA where username ='{}'".format(username))
	usernameList = dbCursor.fetchall()

	# usernameList contains the count of users having same username to currentlr registering 
	# If it is more than 0 then the username is declined and requested to enter another username 
	if int(usernameList[0][0]) > 0:
		clientIdentifier.send("Username not available!!!\nTry different one".encode())
		username = sign_in(clientIdentifier, dbConn)
	else:
		clientIdentifier.send("Password: ".encode())
		password = str(clientIdentifier.recv(1024).decode()).strip()
		
		clientIdentifier.send("Confirm Password: ".encode())
		confirmPassword = str(clientIdentifier.recv(1024).decode()).strip()
		
		if password != confirmPassword:
			clientIdentifier.send("Passwords did not match!!!".encode())
			username = sign_in(clientIdentifier, dbConn)
		else:
			
			dbCursor.execute('''INSERT INTO USERDATA (username, password, name, surname) 
			values ('{}', '{}', '{}', '{}')'''.format(username, password, name, surname))
			
			onlineClients.append(username)	

			# A relation for each registered user is created to store its data
			dbCursor.execute(f'''CREATE TABLE {username} (
				sender text, 
				message text,
				date text,
				time text,
				readreciept int,
				timestamp TIMESTAMP,
				FOREIGN KEY (sender) REFERENCES USERDATA(username));''')
			
			# A function that notifies the user if he is online and a new message is there for him
			# The function is called by a trigger which gets triggered on insertion on its table
			dbCursor.execute(f"""
			CREATE OR REPLACE FUNCTION notifier_{username}()
			RETURNS trigger AS $$
			DECLARE
			BEGIN
				PERFORM pg_notify('{username.lower()}', row_to_json(NEW)::text );
			RETURN NEW;
			END;
			$$ LANGUAGE plpgsql;
			CREATE TRIGGER notify_trigger_{username}
			AFTER INSERT ON {username}
			FOR EACH ROW
			EXECUTE PROCEDURE notifier_{username}();
			""")
			print("User Registered Successfully!!!")
			dbConn.commit()
	return username

class DestClass:
	def __init__(self, destclient):
		self.destclient = destclient		

# to continuously listen the database and notify the user if a new message is there for him
# Execued within a separate thread
def Notifier(username, clientIdentifier, destclient):
	Conn = psycopg2.connect(database="messenger", user="postgres", password="12345678", host="localhost", port=5432)
	Conn.autocommit = True
	Cursor = Conn.cursor()
	Cursor.execute(f"LISTEN {username.lower()};")
	while True:
		if select.select([Conn], [], [], 5) != ([], [], []):
			Conn.poll()
			while Conn.notifies:
				notify = Conn.notifies.pop(0)
				payload = str(notify.payload)
				JSONpayload = json.loads(payload)
				if JSONpayload['sender'] == destclient.destclient:
					payload = payload[:-1] + """, "online": 1}"""
					Cursor.execute(f"UPDATE {username} SET readreciept = 1;")
				clientIdentifier.send(str(payload).encode())
				Conn.commit()

# Function to handle a particular client connection
def Application(clientIdentifier):
	clientIdentifier.send("Select desired alternatives:\n1: to log in\n2: to sign in\nYour choice: ".encode())
	dbHandler = psycopg2.connect(database="messenger", user="postgres", password="12345678", host="localhost", port=5432)
	dbCursor = dbHandler.cursor()
	login_or_signin = clientIdentifier.recv(1024).decode()

	# Keeps the track of unseen messages
	unreadMsgs = 0

	# Keeps the trsack of unread chats
	unreadChats = 0

	if int(login_or_signin) == 1:
		userName = log_in(clientIdentifier, 3, dbCursor, unreadMsgs, unreadChats)
		if not userName:
			return
	elif int(login_or_signin) == 2:
		userName = sign_in(clientIdentifier, dbHandler)
		dbHandler.commit()
	else:
		print("Invalid option!!!\nPlease Try again")	
		Application(clientIdentifier, 3)

	# destclient is the client to whom message is supposed to be sent
	# Its default value is user himself 
	# To change it, use "change <username>" statement  
	destclient = DestClass(userName)

	# Initiates Notifier thread
	notifierThread = threading.Thread(target=Notifier, args=(userName, clientIdentifier, destclient))
	notifierThread.start()

	while True:

		# stores response from client
		recvdMsg = clientIdentifier.recv(1024).decode().strip()
		
		# showOn displays all the online clients
		if recvdMsg == "showOn":
			separator = '\n'
			clientIdentifier.send(separator.join(onlineClients).encode())
			continue

		# showAll displays all the registered clients
		elif recvdMsg == "showAll":
			separator = '\n'
			dbCursor.execute("""SELECT username FROM USERDATA;""")
			allUsers = dbCursor.fetchall()
			users = lambda x: [i[0] for i in x]
			clientIdentifier.send(separator.join(users(allUsers)).encode())
			continue

		# change used to destClient
		# It also marks all the messages from destClients as seen
		elif recvdMsg.split()[0] == "change":
			dbCursor.execute('SELECT username FROM USERDATA;')
			allUsers = dbCursor.fetchall()
			users = lambda x: [i[0] for i in x]
			if recvdMsg.split()[1] in users(allUsers): 
				destclient.destclient = recvdMsg.split()[1]
				dbCursor.execute("SELECT COUNT(readreciept) FROM {} WHERE sender = '{}';".format(userName, destclient.destclient))
				msgsfromsender = int(dbCursor.fetchall()[0][0])
				dbCursor.execute("UPDATE {} SET readreciept = 1 WHERE sender = '{}';".format(userName, destclient.destclient))
				unreadMsgs -= msgsfromsender
				unreadChats -= 1
				dbCursor.execute(f"""CREATE TEMP TABLE chats AS
				SELECT message, timestamp FROM {userName} where sender = '{destclient.destclient}';
				
			    INSERT INTO chats (message,timestamp)
				SELECT message, timestamp
				FROM {destclient.destclient} where sender = '{userName}';
				
				SELECT message FROM chats ORDER BY timestamp asc; 
				""")
				try:
					chats = list(chat[0] for chat in dbCursor.fetchall())
					chats = str('*|*'.join(chats))
				except:
					chats = f"Welcome!!!\nSay Hi to {destclient.destclient}"
				time.sleep(2)
				clientIdentifier.send(chats.encode())
				dbCursor.execute("DROP TABLE chats;")
				continue

		# To close the connection
		elif recvdMsg == "_exit_":
			onlineClients.remove(userName)
			print("Connection terminated for", userName)
			break
		
		# To get brief of unseen messages from various chats
		elif recvdMsg == "checkNewMsgs":
			dbCursor.execute('''SELECT COUNT(DISTINCT sender), COUNT(sender) from {} 
			where readreciept = 0;'''.format(userName))
			readReport = dbCursor.fetchall()
			clientIdentifier.send('''You have {} unread messages from {} chats.'''.format(readReport[0][1], readReport[0][0]).encode())
			continue
		
		# Each message is storeed in respective user's table
		dbCursor.execute('''INSERT INTO {} VALUES ('{}', '{}', CURRENT_DATE, LOCALTIME, 0, LOCALTIMESTAMP)'''.format(destclient.destclient, userName, recvdMsg))
		dbHandler.commit()

try:
	# Creates a socket and if it fails, it will raise an error
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket creation successfull!!!")
except socket.error as err:
	print("Socket creation failed with error", str(err))

# Default port for server 
portNo = 4444


# Bind the socket
try:
	serverSocket.bind(("192.168.1.206", portNo))
	print("Socket has been bound at the port 4444")
except socket.error as err:
	print("Failed to Bind the socket with error", str(err))

# Put the socket in the passive mode
try:
	serverSocket.listen(10)
	print("Server is listening")
except socket.error as err:
	print("Failed to listen with error", str(err))


while True:
	try:
		clientConnection, clientAddr = serverSocket.accept()
		print("Connection established successfully")
	except socket.error:
		print("Connection failed with error", socket.error)

	applicationThread.append(threading.Thread(target=Application, args=(clientConnection,)))
	applicationThread[len(applicationThread)-1].start()
# from os import name
import socket
import threading
import psycopg2
import select
import json
import os
from twilio.rest import Client
import time
import pickle
import string
import math
import random
from decouple import config 


# OTP Generator
def generateOTP():
	digits = "0123456789"
	OTP = ""

	for i in range(4):
		OTP += digits[math.floor(random.random() * 10)]
	
	return OTP


# ChatBot model
def cleaner(x):
    return [a for a in (''.join([a for a in x if a not in string.punctuation])).lower().split()]

traied_model = pickle.load(open('model.sav', 'rb'))

# A list to hold names of users those are online
onlineClients = list()

# A list containing thread ids of each connection thread
applicationThread = list()

# Database name
dataBase = 'scratch'

# Database connector
dbConn = psycopg2.connect(database=dataBase, user="postgres", password="12345678", host="localhost", port=5432)
dbConn.autocommit = True
dbCursor = dbConn.cursor()

# Creates a table that holds each registered user's credentials
try:	
	dbCursor.execute('''CREATE TABLE USERDATA (
		mobNo text PRIMARY KEY,
		username text,
		name text,
		status text);''')
	dbConn.commit()
except:
	print("Error in Creation of Table 'Userdata' or It already exists.") 


# Creates a table that holds each registered user's transactions
try:	
	dbCursor.execute('''CREATE TABLE transactions (
		transactionID SERIAL PRIMARY KEY,
		sender text,
		beneficiary text,
		amount decimal,
		timestamp TIMESTAMP
		);''')
	dbConn.commit()
except:
	print("Error in Creation of Table 'transactions' or It already exists.") 

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

# To carry out the process of registration
def registerMe(clientIdentifier, Conn, userCredentials):
	dbCursor = Conn.cursor()
	
	name = userCredentials['name'].strip()
	mobNo = userCredentials['mobNo'].strip()

	if len(mobNo) > 10:
		clientIdentifier.send("Invalid Phone number!!!".encode())
		clientIdentifier.close()
		return None

	userName = "paigham" + mobNo

	dbCursor.execute("SELECT COUNT(mobNo) from USERDATA where mobNo ='{}'".format(mobNo))
	usernameList = dbCursor.fetchall()
	print(usernameList)
		
	otp = generateOTP()

	client = Client(config('ACCOUNT_SID'), config('AUTH_TOKEN'))
	
	message = client.messages.create(
		body=f'This is your verification code for paigham: {otp}',
		from_=config('PHONE_NUMBER'),
		to=f'+91{mobNo}'
	)

	print(message.sid)

	returnedOTP = clientIdentifier.recv(1024).decode().strip()


	# if str(otp) == returnedOTP:
	if "1234" == returnedOTP:

		# usernameList contains the count of users having same username to currentlr registering 
		# If it is more than 0 then the username is declined and requested to enter another username 
		if int(usernameList[0][0]) > 0:
			clientIdentifier.send("userAlreadyRegisteredx911".encode())
		else:
			dbCursor.execute('''INSERT INTO USERDATA (mobNo, username, name) 
			values ('{}', '{}', '{}')'''.format(mobNo, userName, name))
			
			
			onlineClients.append(userName)	

			# A relation for each registered user is created to store its data
			dbCursor.execute(f'''CREATE TABLE {userName} (
				sender text, 
				message text,
				date text,
				time text,
				readreciept int,
				timestamp TIMESTAMP,
				FOREIGN KEY (sender) REFERENCES USERDATA(mobNo));''')
			
			
			# A function that notifies the user if he is online and a new message is there for him
			# The function is called by a trigger which gets triggered on insertion on its table
			dbCursor.execute(f"""
			CREATE OR REPLACE FUNCTION notifier_{userName}()
			RETURNS trigger AS $$
			DECLARE
			BEGIN
				PERFORM pg_notify('{userName.lower()}', row_to_json(NEW)::text );
			RETURN NEW;
			END;
			$$ LANGUAGE plpgsql;
			CREATE TRIGGER notify_trigger_{userName}
			AFTER INSERT ON {userName}
			FOR EACH ROW
			EXECUTE PROCEDURE notifier_{userName}();
			""")
			print("User Registered Successfully!!!")
			clientIdentifier.send(userName.encode())
			Conn.commit()
	else:
		clientIdentifier.send("Invalid OTP!!!".encode())

	return userName
	


class DestClass:
	def __init__(self, destclient):
		self.destclient = destclient		

# to continuously listen the database and notify the user if a new message is there for him
# Execued within a separate thread
def Notifier(username, clientIdentifier, destclient):
	Conn = psycopg2.connect(database=dataBase, user="postgres", password="12345678", host="localhost", port=5432)
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
					print(str(payload))
				clientIdentifier.send(str(payload).encode())
				Conn.commit()

# Function to handle a particular client connection
def Application(clientIdentifier):
	dbHandler = psycopg2.connect(database=dataBase, user="postgres", password="12345678", host="localhost", port=5432)
	dbCursor = dbHandler.cursor()
	
	userCredentials = clientIdentifier.recv(1024).decode().strip()
	print(userCredentials)
	userCredentials = eval(userCredentials)
	print(userCredentials)

	# Keeps the track of unseen messages
	unreadMsgs = 0

	# Keeps the trsack of unread chats
	unreadChats = 0

	
	# Register client if he/she is new
	userName = registerMe(clientIdentifier, dbHandler, userCredentials)
	print(userName)

	# destclient is the client to whom message is supposed to be sent
	# Its default value is user himself 
	# To change it, use "change <username>" statement  
	destclient = DestClass(userName)

	# Initiates Notifier thread
	notifierThread = threading.Thread(target=Notifier, args=(userName, clientIdentifier, destclient))
	notifierThread.start()

	while True:

		"""###################################  recvdMsg  #################################
		recvdMsg = {
			'command': a text depicting what to do,
			'message': a text message to be forwarded to its destination,
			'destClient': mobNo of destClient whose file descriptor has to be fetched from userdata table,
			'msgType': a text depicting type of message that it contains 
		}
		######################################  recvdMsg  #################################"""
		# stores response from client
		recvdMsg = clientIdentifier.recv(1024).decode().strip()
		print(recvdMsg)
		recvdMsg = eval(recvdMsg)
		
		# change used to destClient
		# It also marks all the messages from destClients as seen
		if recvdMsg['command'] == "transact":
			print(recvdMsg['message'], "\n", type(recvdMsg['message']))
			data = eval(str(recvdMsg['message']))
			dbCursor.execute(f"""INSERT INTO transactions (sender, beneficiary, amount, timestamp) values ('{data['sender']}', '{data['beneficiary']}', {data['amount']}, LOCALTIMESTAMP);""")
			dbHandler.commit()
			clientIdentifier.send("Transaction Successful!!!".encode())
		
		elif recvdMsg['command'] == "viewBal":
			data = recvdMsg['message']
			dbCursor.execute(f"""SELECT SUM(amount) FROM transactions WHERE beneficiary='{data['me']}';""")
			incoming = float(dbCursor.fetchall()[0][0])
			dbCursor.execute(f"""SELECT SUM(amount) FROM transactions WHERE sender='{data['me']}';""")
			outgoing = float(dbCursor.fetchall()[0][0])
			clientIdentifier.send(f"Your Balance: {str(incoming-outgoing)}".encode())

		elif recvdMsg['command'] == "getTransList":
			data = recvdMsg['message']
			dbCursor.execute(f"""CREATE TEMP TABLE transhistory AS 
			SELECT * FROM transactions where sender='{data['me']}';

			INSERT INTO transhistory (transactionID, sender, beneficiary, amount, timestamp) 
			SELECT * FROM transactions where beneficiary='{data['me']}';
			
			SELECT * FROM transhistory ORDER BY timestamp asc;""")

			try:
				transHistory = list(x[0] for x in dbCursor.fetchall())
				transHistory = str('*|*'.join(transHistory))
			except:
				transHistory = "No transaction history exists!"
			
			time.sleep(2)
			clientIdentifier.send(transHistory.encode())
			dbCursor.execute("DROP TABLE transhistory;")
			dbHandler.commit()

		elif recvdMsg['command'] == "delAcc":
			data = recvdMsg['message']
			dbCursor.execute(f"""DELETE FROM USERDATA WHERE mobNo='{data['me']}';""")
			dbCursor.execute(f"DROP TABLE paigham{data['me']} CASCADE;")
			dbHandler.commit()
			clientIdentifier.send(f"{data['me']} deleted!!!".encode())

		elif recvdMsg['command'] == "chngStat":
			data = recvdMsg['message']
			dbCursor.execute(f"UPDATE USERDATA SET status='{data['newStat']}' WHERE mobNo = '{data['me']}';")
			dbHandler.commit()
			clientIdentifier.send(f"Status changed to {data['newStat']}.".encode())

		elif recvdMsg['command'] == "change":
			dbCursor.execute('SELECT username FROM USERDATA;')
			allUsers = dbCursor.fetchall()
			users = lambda x: [i[0] for i in x]
			if "paigham"+recvdMsg['to'] in users(allUsers): 
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
				dbHandler.commit()
				continue

		elif recvdMsg['msgType'] == 'chatBotMsg':
			replyText = traied_model.predict([recvdMsg['message']])[0]
			print(replyText)
			clientIdentifier.send(replyText.encode())
		
		# Each message is stored in respective user's table
		elif recvdMsg['msgType'] == 'textMsg': 
			dbCursor.execute('''INSERT INTO paigham{} VALUES ('paigham{}', '{}', CURRENT_DATE, LOCALTIME, 0, LOCALTIMESTAMP)'''.format(recvdMsg['destClient'], recvdMsg['destClient'], recvdMsg['message'], recvdMsg))
			dbHandler.commit()
			clientIdentifier.send("Double tick!".encode())

		elif recvdMsg['msgType'] == 'binaryMedia':
			pass
			"""#########################	Please complete this part	#######################"""
		
		dbHandler.commit()

try:
	# Creates a socket and if it fails, it will raise an error
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket creation successfull!!!")
except socket.error as err:
	print("Socket creation failed with error", str(err))

# Default port for server 
portNo = 4444
ipAddr = "192.168.1.201"


# Bind the socket
try:
	serverSocket.bind((ipAddr, portNo))
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
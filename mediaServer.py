import socket
import threading
import psycopg2
import time
from math import *

# Database connector
###########################             UNCOMMENT IF YOU WANT TO USE DATABASE              #################################
# dbConn = psycopg2.connect(database="", user="", password="", host="localhost", port=5432)
# dbConn.autocommit = True
# dbCursor = dbConn.cursor()

# clientList holds socket connection object of each connection with key equal to 'paigham' followed by user's mobile number
clientList = dict()

# threadlist holds the thread id of each independent thread running on server
threadList = list()

# reates a table to store files
###########################             UNCOMMENT IF YOU WANT TO STORE EACH BINARY FILE              #################################
# try: 
# 	dbCursor.execute("""
# 	CREATE TABLE mediafiles (
# 		timestamp TIMESTAMP,
# 		extension text,
# 		media bytea
# 	);
# 	""")
# except:
# 	pass

# router function is executed by the thread and it routes the binary file to its desired receiver
def router(clientConnection):
	
	while True:

		# receives desired receiver's mobile number
		destClientMobNo = clientConnection.recv(2048).decode()

		# using the receiver's mobile number, his/her unique key is generated and his/her socket connection object is obtained
		destConnection = clientList[f"paigham{destClientMobNo}"]

		# incoming file's extension is receieved
		file_ext = "." + clientConnection.recv(2048).decode().strip()

		# incoming file's extension is sent to receiver
		destConnection.send(file_ext.encode())



		# stores binary syring of received biney file 
		###########################         UNCOMMENT IF YOU WANT TO STORE EACH BINARY FILE           #################################
		# mediaBinary = b""


		# receives first chunk of incoming binary file
		byteChunk = clientConnection.recv(2048)

		# byteSent keeps the track of total number of bytes sent
		byteReceived = 2048
		
		while byteChunk:
			# mediaBinary += byteChunk                              # UNCOMMENT IF YOU WANT TO STORE EACH BINARY FILE
			
			# routing is performed
			destConnection.send(byteChunk)
			byteChunk = clientConnection.recv(2048)
			try:
				# checking whether a 0 is received or not
				byteChunk = int(byteChunk.decode().strip())
			except:
				pass
			
			byteReceived += 2048

		# sleeps till server receives the entire file
		# the value '774144' is experimentally determined 
		time.sleep(ceil(byteReceived / 774144))

		# send the 0 which later gets converted to integer 0 and stops the receiver mechanism on client's end
		destConnection.send("0".encode())
		print("File received !!!")

		# inserts received binary file into database
		###########################         UNCOMMENT IF YOU WANT TO STORE EACH BINARY FILE           #################################
		# dbCursor.execute(f"""INSERT INTO mediafiles (timestamp, extension, media) VALUES( LOCALTIMESTAMP, %s, %s)""", (file_ext, psycopg2.Binary(mediaBinary)))
		# dbConn.commit


		# fetches stored binary file from database
		# you can use timestamp to identify correct file
		###########################         UNCOMMENT IF YOU WANT TO STORE EACH BINARY FILE           #################################
		# dbCursor.execute("SELECT extension, media FROM mediafiles;")
		# blob = dbCursor.fetchall()[-1]
		# open(f'received{blob[0]}', 'wb').write(blob[1])





try:
	# Creates a socket and if it fails, it will raise an error
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket creation successfull!!!")
except socket.error as err:
	print("Socket creation failed with error", str(err))


# Default socket for server 
portNo = 4445
ipAddr = "192.168.1.202"


# Bind the socket
try:
	serverSocket.bind((ipAddr, portNo))
	print(f"Socket has been bound at the port {portNo}")
except socket.error as err:
	print("Failed to Bind the socket with error", str(err))

# Put the socket in the passive mode
try:
	serverSocket.listen(10)
	print("Server is listening")
except socket.error as err:
	print("Failed to listen with error", str(err))



while True:
	# clientConnection, clientAddr = serverSocket.accept()
	try:
		clientConnection, clientAddr = serverSocket.accept()
		print("Connection established successfully")
	except socket.error:
		print("Connection failed with error", socket.error)
		break

	# gets the information of connected user in the form of dictionary string
	userInfo = clientConnection.recv(1024).decode()

	# converts received dictionary string into dictionary
	userInfo = eval(userInfo)
	###################################     Registration Authentication     #####################################

	###################################     Registration Authentication     #####################################

	# inserts the connection object into clientList using a unique key
	clientList[f"paigham{userInfo['MobNo']}"] = clientConnection

	# multi-threading router system starts here
	threadList.append(threading.Thread(target=router, args=(clientConnection,)))
	threadList[len(threadList)-1].start()

clientConnection.close()
from math import ceil
from typing import Counter
import psycopg2


# Database connector
dbConn = psycopg2.connect(database="scratch", user="postgres", password="12345678", host="localhost", port=5432)
dbConn.autocommit = True
dbCursor = dbConn.cursor()

##############################         DO NOT DELETE FOLLOWING CONTENT              ###############################


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

# path =  "C:/Users/ojasp/Pictures/a.png"
# file_ext = path.split('.')[-1]
# f = open("C:/Users/ojasp/Pictures/a.png", 'rb').read()
# dbCursor.execute(f"""INSERT INTO mediafiles (timestamp, extension, media) VALUES( LOCALTIMESTAMP, %s, %s)""", (file_ext, psycopg2.Binary(f)))
# dbConn.commit()

# dbCursor.execute("SELECT media, extension FROM mediafiles")
# blob = dbCursor.fetchall()[-1]
# print(blob)
# open(f'fetched.png', 'wb').write(blob[0])

#################################################################################################################

# dbCursor.execute("TRUNCATE mediafiles;")
dbConn.commit()
import socket
import threading
import psycopg2
import time

# Database connector
dbConn = psycopg2.connect(database="scratch", user="postgres", password="12345678", host="localhost", port=5432)
dbConn.autocommit = True
dbCursor = dbConn.cursor()


clientList = dict()
threadList = list()


try: 
	dbCursor.execute("""
	CREATE TABLE mediafiles (
		timestamp TIMESTAMP,
		extension text,
		media bytea
	);
	""")
except:
	pass



def router(clientConnection, userInfo):
	
	while True:
		destClientMobNo = clientConnection.recv(2048).decode()
		destConnection = clientList[f"paigham{destClientMobNo}"]


		mediaBinary = b""

		imgChunk = clientConnection.recv(2048)
		byteReceived = 2048
		startTime = time.time()
		while imgChunk:
			mediaBinary += imgChunk
			destConnection.send(imgChunk)
			imgChunk = clientConnection.recv(2048)
			try:
				imgChunk = int(imgChunk.decode().strip())
			except:
				pass
			
			byteReceived += 2048

		print("time taken: ", time.time() - startTime)
		
		time.sleep(ceil(byteReceived/ 774144))

		destConnection.send("0".encode())

		dbCursor.execute(f"""INSERT INTO mediafiles (timestamp, extension, media) VALUES( LOCALTIMESTAMP, %s, %s)""", (file_ext, psycopg2.Binary(mediaBinary)))

		dbConn.commit

		dbCursor.execute("SELECT extension, media FROM mediafiles;")
		blob = dbCursor.fetchall()[-1]
		
		open(f'received{blob[0]}', 'wb').write(blob[1])





try:
	# Creates a socket and if it fails, it will raise an error
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket creation successfull!!!")
except socket.error as err:
	print("Socket creation failed with error", str(err))


# Default socket for server 
portNo = 4445
ipAddr = "192.168.1.201"


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



file_ext = ".png"

while True:
	# clientConnection, clientAddr = serverSocket.accept()
	try:
		clientConnection, clientAddr = serverSocket.accept()
		print("Connection established successfully")
	except socket.error:
		print("Connection failed with error", socket.error)
		break
	
	userInfo = clientConnection.recv(1024).decode()
	userInfo = eval(userInfo)
	###################################     Registration Authentication     #####################################

	###################################     Registration Authentication     #####################################

	clientList[f"paigham{userInfo['MobNo']}"] = clientConnection
	threadList.append(threading.Thread(target=router, args=(clientConnection, userInfo)))
	threadList[len(threadList)-1].start()

clientConnection.close()
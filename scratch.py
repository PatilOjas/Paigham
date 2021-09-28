import socket
import threading
import psycopg2
import os

# Database connector
dbConn = psycopg2.connect(database="scratch", user="postgres", password="12345678", host="localhost", port=5432)
dbConn.autocommit = True
dbCursor = dbConn.cursor()


counter = 0
clientList = dict()
threadList = list()


def router(clientConnection, userInfo):
	global counter
	
	while True:
		counter += 1
		destClientMobNo = clientConnection.recv(2048).decode()
		print("destClientConnection", clientList[f"paigham{destClientMobNo}"])
		destConnection = clientList[f"paigham{destClientMobNo}"]


		# f = open(f'recvdImgServer.mp4', 'wb')
		imgChunk = clientConnection.recv(2048)
		while imgChunk:
			# f.write(imgChunk)
			destConnection.send(imgChunk)
			imgChunk = clientConnection.recv(2048)
		
		# f.seek(0)

		# imgData = f.read(2048)
		# while imgData:
		# 	destConnection.send(imgData)
		# 	imgData = f.read(2048)
		
		# f.close()

		# f = open(f'recvdImg{counter}.png', 'rb').read()
		# dbCursor.execute(f"""INSERT INTO images (id, ext, image) VALUES(%s, %s, %s)""", (counter, file_ext, psycopg2.Binary(f)))

		# dbConn.commit

		# os.remove(f'recvdImg{counter}.png')
		counter-=1
		# dbCursor.execute("SELECT id, image, ext FROM images WHERE id=2;")
		# blob = dbCursor.fetchone()

		# print(blob)

		# open('fetched.png', 'wb').write(blob[1])





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
	print("Socket has been bound at the port 4444")
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
	
	print("clientConnection: ", clientConnection)
	userInfo = clientConnection.recv(1024).decode()
	userInfo = eval(userInfo)
	print(userInfo)
	#######################################           Registration Authentication           #########################################

	#######################################           Registration Authentication           #########################################

	clientList[f"paigham{userInfo['MobNo']}"] = clientConnection
	print("clientList: ", clientList)
	threadList.append(threading.Thread(target=router, args=(clientConnection, userInfo)))
	threadList[len(threadList)-1].start()

clientConnection.close()
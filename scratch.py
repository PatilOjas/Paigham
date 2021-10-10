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

import socket
import time

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

	# This line passes received extension of file to destination
	# You can use any one of server file for routing but keep time.sleep(0.1) or greater for extension passing
	# Else data gets concatenated at dart client side  
	clientConnection.send(clientConnection.recv(2048).strip())
	time.sleep(0.1)
	
	# To count excution time
	startTime = time.time()

	# receives first bytes  
	byteImage = clientConnection.recv(2048)
	
	# Route until condition becomes false by byteImage = 0
	while byteImage:
		clientConnection.send(byteImage)
		byteImage = clientConnection.recv(2048)
		try:
			# checking whether a 0 is received or not
			if byteImage == b'0':
				print(True)
				print(str(byteImage), type(byteImage)) 
			byteImage = int(byteImage.decode().strip())
		except:
			pass


	time.sleep(2)
	print("time elapsed: ", time.time() - startTime)
	print("Done")

clientConnection.close()

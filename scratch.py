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
ipAddr = "192.168.1.205"


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

# clientConnection, clientAddr = serverSocket.accept()
try:
	clientConnection, clientAddr = serverSocket.accept()
	print("Connection established successfully")
except socket.error:
	print("Connection failed with error", socket.error)
		
f = open('file.mp4', 'wb')
print(clientConnection.recv(2048).decode().strip())

startTime = time.time()

byteSent  = 2048

byteImage = clientConnection.recv(2048)

while byteImage:
	f.write(byteImage)
	# print(byteImage)
	byteImage = clientConnection.recv(2048)
	try:
		# checking whether a 0 is received or not
		if byteImage == b'0':
			print(True)
			print(str(byteImage), type(byteImage)) 
		byteImage = int(byteImage.decode().strip())
	except:
		pass
	byteSent += 2048
	print(byteSent)

print("bytes received: ", byteSent)
print("time elapsed: ", time.time() - startTime)
print("Done", byteImage, type(byteImage))
clientConnection.send("Thank You for the image".encode())
clientConnection.close()
f.close()
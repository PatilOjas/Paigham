import socket
import threading
import time
from math import *
import re
import datetime

# myInfo stores the information of the user such as his/ her mobile numer
myInfo = dict()

# Function that will continuiously receive binary files
def receiver(clientSocket):

	while True:
		
		# receive file extension of incoming files
		file_ext = clientSocket.recv(2048).decode().strip()

		# receives first chunk of incoming file
		byteChunk = clientSocket.recv(2048)

		# filename using current timestamp
		fileName = re.sub('[ :, .]', '', re.sub('[\s]', '-', str(datetime.datetime.now())))

		# opens a binary file with name equal to current timestamp
		f = open(f"{fileName}{file_ext}", 'wb')

		# complete file receiver mechanism
		while byteChunk:
			f.write(byteChunk)
			byteChunk = clientSocket.recv(2048)

			# tries to convert each byte to int in order to make the loop condition false and stop the iteration
			try:
				byteChunk = int(byteChunk.decode().strip())
			except:
				pass
		f.close()
		print("File received!!!")
		

try:
	# Creates a socket and if it fails, it will raise an error
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket creation successfull!!!")
except socket.error:
	print("Socket creation failed with error", str(socket.error))

# Default port for server 
portNo = 4445
ipAddr = "192.168.1.201"

# Connects to server
try:
	clientSocket.connect((ipAddr, portNo))
	print("Connection successfull!!!")
except socket.error:
	print("Failed to connect with error", socket.error)




myMobNo = str(input("Enter your mobile number: "))
myInfo['MobNo'] = myMobNo

clientSocket.send(str(myInfo).encode())


# multi-threading starts here
tid = threading.Thread(target=receiver, args=(clientSocket,))
tid.start()


# infinite loop to send binary files
while True:

	destMobNo = str(input("Enter receiver's mobile no: "))
	clientSocket.send(destMobNo.encode())

	fileToBeSent = str(input("Enter the name of file to be sent (with extension): "))

	# separates and sends the file extension to server
	clientSocket.send(fileToBeSent.split('.')[-1].encode())

	# opens and reads the binary file to be sent
	f = open(f'{fileToBeSent}', 'rb')

	# byteSent keeps the track of total number of bytes sent 
	byteSent = 2048

	# byteData reads consecutive 2048 bytes of the file
	byteData = f.read(2048)

	# file sending mechanism
	while byteData:
		clientSocket.send(byteData)
		byteData = f.read(2048)
		byteSent += 2048

	f.close()

	# sleeps till server receives the entire file
	# the value '774144' is experimentally determined 
	time.sleep(ceil(byteSent/774144))

	# send the 0 which later gets converted to integer 0 and stops the receiver mechanism on server's end
	clientSocket.send("0".encode())
	
clientSocket.close()



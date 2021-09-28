import socket
import threading

counter = 0
def receiver(clientSocket):
	global counter
	imgChunk = clientSocket.recv(2048)
	while True:
		f = open(f'recvdImg{counter}.pdf', 'wb')
		while imgChunk:
			f.write(imgChunk)
			imgChunk = clientSocket.recv(2048)
		f.close()
		# counter += 1

try:
	# Creates a socket and if it fails, it will raise an error
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket creation successfull!!!")
except socket.error:
	print("Socket creation failed with error", str(socket.error))

# Default port for server 
portNo = 4445

# Connects to server
try:
	clientSocket.connect(("192.168.1.201", portNo))
	print("Connection successfull!!!")
except socket.error:
	print("Failed to connect with error", socket.error)

myInfo = dict()

myMobNo = str(input("Enter your mobile number: "))
myInfo['MobNo'] = myMobNo

clientSocket.send(str(myInfo).encode())

tid = threading.Thread(target=receiver, args=(clientSocket,))
tid.start()

while True:

	destMobNo = str(input("Enter receiver's mobile no: "))
	clientSocket.send(destMobNo.encode())

	fileToBeSent = str(input("Enter the name of file to be sent (with extension): "))

	f = open(f'./{fileToBeSent}', 'rb')
	imgData = f.read(2048)

	while imgData:
		clientSocket.send(imgData)
		imgData = f.read(2048)

	f.close()
	print("Document closed")
clientSocket.close()



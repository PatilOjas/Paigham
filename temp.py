import socket

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

try:
	clientConnection, clientAddr = serverSocket.accept()
	print("Connection established successfully")
except socket.error:
	print("Connection failed with error", socket.error)
	
print("listening...")
x = clientConnection.recv(2048).decode().strip()
print(x)
q = int(x)
print(type(q), q)
if q:
	print("binary space is true")
else:
	print("space is false")
# print(clientConnection.recv(2048))
print("listening again...")
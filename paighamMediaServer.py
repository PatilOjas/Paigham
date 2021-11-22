import socket
import time
import psycopg2

# Database name
dataBase = 'scratch'

# Database connector
dbConn = psycopg2.connect(database=dataBase, user="postgres", password="12345678", host="localhost", port=5432)
dbConn.autocommit = True
dbCursor = dbConn.cursor()


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
	try:
		clientConnection, clientAddr = serverSocket.accept()
		print("Connection established successfully")
	except socket.error:
		print("Connection failed with error", socket.error)

	# This line passes received metadata of file to destination
	# You can use any one of server file for routing but keep time.sleep(0.1) or greater for extension passing
	# Else data gets concatenated at dart client side
	metaData = clientConnection.recv(2048).strip()  
	clientConnection.send(metaData)
	metaData = eval(metaData)
	time.sleep(0.2)

	# first send the metadate to server which will help to fetch file descriptor from userdata table
	
	"""	###############################	  METADATA	##################################	
		metaData = {
			'destClient': mobNo of destClient whose file descriptor has to be fetched from userdata table
			'extension': extension of file to be transferred
		}
		###############################	  METADATA	##################################	
	"""

	# get filedescriptor from userdata table
	dbCursor.execute(f"SELECT filedesc FROM TABLE userdata WHERE mobNo = '{metaData['destClient']}'")
	tempFetchedData = dbCursor.fetchall()

	destClient = b""

	if len(tempFetchedData) > 0 and tempFetchedData[0] != None:
		destClient = tempFetchedData[0]
	else:
		"""#######################	Notify client	############################"""

		"""#######################	Notify client	############################"""
		break


	# To count excution time
	startTime = time.time()

	# receives first chunk bytes  
	byteImage = clientConnection.recv(2048)
	
	# Route until condition becomes false by byteImage = 0
	while byteImage:
		destClient.send(byteImage)
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

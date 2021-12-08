import pytest
import socket
import time

class Test:
	def getOTP(self,):
		cliSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cliSocket.connect(("192.168.1.201", 4444))

		cliSocket.send("""
		{
			'name': 'Ojas',
			'mobNo': '9619542526',
		}
		""".encode())
		time.sleep(2)
		cliSocket.send("1234".encode())
		recvdData = cliSocket.recv(1024).decode().strip()
		cliSocket.close()
		return recvdData

	def test_getOTP1(self,):
		recvdData = self.getOTP()
		assert recvdData == "paigham9619542526" 

	def test_getOTP2(self,):
		recvdData = self.getOTP()
		assert recvdData == "userAlreadyRegisteredx911" 
		
	def test_getOTP3(self,):
		recvdData = self.getOTP()
		assert recvdData == "Invalid OTP!!!"

	def test_getOTP4(self,):
		recvdData = self.getOTP()
		assert recvdData == "Invalid Phone number!!!"


	def reply(self,additionalData):
		cliSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cliSocket.connect(("192.168.1.201", 4444))

		cliSocket.send("""
		{
			'name': 'Ojas',
			'mobNo': '9619542526',
		}
		""".encode())
		time.sleep(2)
		cliSocket.send("1234".encode())
		cliSocket.recv(1024).decode().strip()
		msg = """{
				'name': 'Ojas',
				'mobNo': '9619542526',
				""" + additionalData + """ } """
		time.sleep(2)
		cliSocket.send(msg.encode())
		time.sleep(2)
		recvdReply = cliSocket.recv(1024).decode().strip()
		return recvdReply

		

	def test_chatBotReply(self,):
		recvdReply = self.reply("""'msgType': 'chatBotMsg',
				'message': 'how are you',
				'command': ''""")
		assert recvdReply == "i'm fine. how about yourself?"

	# test_chatBotReply()

	def test_transaction(self,):
		recvdReply = self.reply("""
			'message': {
				'sender': '1234567890',
				'beneficiary': '9619542526',
				'amount': 500,
			},
			'command': 'transact'
		""")
		assert recvdReply == "Transaction Successful!!!"

	def test_viewBal(self,):
		recvdReply = self.reply("""
			'message': {
				'me': '9619542526',
			},
			'command': 'viewBal'
		""")
		assert " ".join(recvdReply.split()[:2]) == "Your Balance:"

	def test_chngStat(self,):
		recvdReply = self.reply("""
			'message': {
				'me': '9619542526',
				'newStat': 'Hey there! I am using Paigham' 
			},
			'command': 'chngStat'
		""")
		assert recvdReply == "Status changed to Hey there! I am using Paigham." 


	def test_textMsg(self,):
		recvdReply = self.reply("""
			'message': 'Hii Hrusheekesh!',
			'destClient': '1234567890',
			'msgType': 'textMsg',
			'command': '',
		""")
		assert recvdReply == "Double tick!"

t = Test()
t.test_getOTP2()
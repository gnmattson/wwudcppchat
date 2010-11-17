from threading import Thread
import socket, array, time, string

class linkToDCPP(Thread):
	"""Thread to receive from server and post to DCPP"""
	#This does not currently ever receive anything from the linking server
	def __init__(self, dcpp_connection):
		Thread.__init__(self)
		self.dcpp_conn = dcpp_connection
		#linking server parameters
		self.server = "localhost"
		self.port = 7014
		self.address = (self.server, self.port)
		self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.UDPSock.connect(self.address)
	#end __init__
	
	def read(self):
		print "in read in linkToDCPP\n"
		buff = ""
		try:
			buff += self.UDPSock.recv(1024)
			return buff
		except socket.error, msg:
			return
	#end read
	
	def run(self):
		print "in run in linkToDCPP\n"
		while True:
			buff = self.read()
			print "message read in linkToDCPP\n"
			#output message to DCPP chat
			self.dcpp_conn.send(buff)
	#end run
	
#end linkToDCPP
	
class linkFromDCPP(Thread):
	"""Thread to send data to server from DCPP"""
	def __init__(self, dcpp_connection, nick):
		Thread.__init__(self)
		self.startLinking = False
		self.dcpp_conn = dcpp_connection
		self.nick = nick
		self.debugflag = 1
		#linking server parameters
		self.server = "localhost"
		self.port = 7015
		self.address = (self.server, self.port)
		self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.UDPSock.connect(self.address)
	#end __init__
	
	def read(self):
		print "in read in linkFromDCPP\n"
		buff = ""
		try:
			buff += self.dcpp_conn.recv(1024)
			return buff
		except socket.error, msg:
			return
	#end read
	
	def lock2key2(self, lock):
		"Decrypts lock to key."
		key = {}
		for i in xrange(1, len(lock)):
			key[i] = ord(lock[i]) ^ ord(lock[i-1])
		key[0] = ord(lock[0]) ^ ord(lock[len(lock)-1]) ^ ord(lock[len(lock)-2]) ^ 5
		for i in xrange(0, len(lock)):
			key[i] = ((key[i]<<4) & 240) | ((key[i]>>4) & 15)
		out = ""
		for i in xrange(0, len(key)):
			if key[i] in (0, 5, 36, 96, 124, 126):
				out += "/%%DCN%03d%%/" % (key[i],)
			else:
				out += chr(key[i])
		return out
	# end lock2key2
	
	def dispatch(self, message):
		print "in dispatch in linkFromDCPP\n"
		if not message:
			return
		#will want to modify this later to match new linker syntax
		if message[0] == '<' and message[1] != '@':
			self.UDPSock.send("**DCPP**"+message)
			print "**to server** sending message..."
		
		#for connecting to dcpp hub
		datalist = message.split()
		if (message) and self.debugflag == 1:
			print message
		if datalist[0] == "|":
			pass
		elif datalist[1] == "YnHub":
			self.startLinking = True
		elif datalist[0] == '$Lock' :
			self.dcpp_conn.send('$Key '+self.lock2key2(datalist[1])+'|')
			print '$Key '+self.lock2key2(datalist[1])+'|'
			self.dcpp_conn.send('$ValidateNick '+self.nick+'|')
			print '$ValidateNick '+self.nick+'|'
		elif  (datalist[0] == '$Hello'):
			info = '$MyINFO $ALL '+self.nick+' I am a chat linker3>$DSL?$no@spam.thx$2147483648$|'
			print info
			self.dcpp_conn.send(info)    
		return
	# end dispatch
	
	def run(self):
		print "in run in linkFromDCPP\n"
		while True:
			#read from dcpp socket and send to linking server
			buff = self.read()
			self.dispatch(buff)
	#end run
		
#end linkFromDCPP

#main
if __name__ == "__main__":
	server = "wwb.wwudc.com"
	port = 411
	nick = "mrpersonLINK"
	address = (server, port)
	DCPPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	DCPPSock.connect(address)
	server_to_dcpp = linkToDCPP(DCPPSock)
	dcpp_to_server = linkFromDCPP(DCPPSock, nick)
	server_to_dcpp.start()
	dcpp_to_server.start()
	#may want to work on closing the connection with dc here
	#otherwise nick has to be changed on each connect with dc
#end main
import socket, array, time, string

class DCPPBot(object):
	"""A DCPP bot"""
	
	# DCPP parameters
	HOST = 'wwb.wwudc.com'
	PORT = 411
	nick = 'mrpersonLINK'
	debugflag = 1
	loggedon =(0)
	startLinking = False
	DCPPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# linking server parameters
	localServer = "localhost"
	localPort = 7015
	address = (localServer, localPort)
	UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	def read(self):
		buff = ""
		try:
			buff += self.DCPPSock.recv(1024)
			return buff
		except socket.error, msg:
			return

		return buff
	# end read
	
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
	
	def connect(self, socket):
		self.DCPPSock.connect((self.HOST, self.PORT))
		return
	# end connect
	
	def dispatch(self, message):
		if not message:
			return
			
		if message[0] == '<' and self.nick != message[1:7] and self.startLinking:
			self.UDPSock.sendto("**DCPP**"+message, self.address) #)
			print "**to server** sending message..."
		
		datalist = message.split()
		
		if (message) and self.debugflag == 1:
			print message
		if datalist[0] == "|":
			pass
		elif datalist[1] == "YnHub":
			self.startLinking = True
		elif datalist[0] == '$Lock' :
			self.DCPPSock.send('$Key '+self.lock2key2(datalist[1])+'|')
			print '$Key '+self.lock2key2(datalist[1])+'|'
			self.DCPPSock.send('$ValidateNick '+self.nick+'|')
			print '$ValidateNick '+self.nick+'|'
		elif  (datalist[0] == '$Hello'):
			self.loggedon = 1
			print '$MyINFO $ALL '+self.nick+' I am a chat linker3>$DSL?$no@spam.thx$2147483648$|'
			self.DCPPSock.send('$MyINFO $ALL '+self.nick+' I am a chat linker3>$DSL?$no@spam.thx$2147483648$|')    
		return
	# end dispatch
	
	def linkParse(self, message):
		if not message:
			return
		
		if message[0:7] == '**IRC**':
			self.DCPPSock.send('<'+self.nick+'> '+message+'|')
			print "linking message..."
		
		#datalist = message.split();
	# end linkParse
   
	def run(self):
		self.connect(self.DCPPSock)
		self.UDPSock.connect(self.address)
		while 1:
			self.dispatch(self.read())
		return
	# end run
# end DCPPBot

# main		
bot = DCPPBot()
bot.run()
# end main

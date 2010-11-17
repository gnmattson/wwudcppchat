from threading import Thread
import socket, string
import irc

class linkToIRC(Thread):
	"""Thread to receive from server and post to IRC"""
	#This does not currently ever receive anything from the linking server
	def __init__(self, irc_connection):
		Thread.__init__(self)
		self.irc_conn = irc_connection
		#linking server parameters
		self.server = "localhost"
		self.port = 7012
		self.address = (self.server, self.port)
		self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.UDPSock.connect(self.address)
	#end __init__
		
	def read(self):
		print "in read in linkToIRC\n"
		buffer = ""
		try:
			buffer += self.UDPSock.recv(1024)
			return buffer
		except socket.error, msg:
			return
	#end read
	
	def run(self):
		while True:
			buff = self.read()
			print "message read in linkToIRC\n"
			#output message to IRC chat
			print buff
			irc.message(self.chan, buff)
			
#end linkToIRC

class linkFromIRC(Thread):
	"""Thread to send messages to server from IRC"""
	def __init__(self, irc_connection):
		Thread.__init__(self)
		self.irc_conn = irc_connection
		#linking server parameters
		self.server = "localhost"
		self.port = 7013
		self.address = (self.server, self.port)
		self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.UDPSock.connect(self.address)
		self.loggedOn = False
	#end __init__
	
	def read(self):
		print "in linkFromIRC read\n"
		buff = ""
		try:
			buff += self.irc_conn.recv(1024)
			return buff
		except socket.error, msg:
			return
		return buff
	# end read
	
	def parse(self, message):
		print "in linkFromIRC parse\n"
		if not message:
			return
		message = string.split(message, "\n")

		for line in message:
			line = string.rstrip(line)
			print line
			line = string.split(line)
			try:
				if line[0] == "PING":
					irc.serverMessage("PONG %s" % line[1])
				elif line[4] == ":End":
					self.loggedOn = True

				if self.loggedOn:
					message = irc.linkParse(line)
					if message:
						self.UDPSock.send("**IRC**"+message)
			except IndexError:
				pass

		return True
	#end parse
	
	def run(self):
		while True:
			self.parse(self.read())
	#end run
#end linkFromIRC

# IRC parameters
server = "irc.freenode.net"
port = 6667
nick = "Linker"
channel = "#wwu-dcpp"
IRCSock = socket.socket()
irc.s = IRCSock

def IRCconnect(server, port, nick):
	ident = nick
	host = nick
	realname = nick
	IRCSock.connect((server, port))
	irc.serverMessage("NICK %s" % nick)
	irc.serverMessage("USER %s %s bla :%s" % (ident, host, realname))
	return True
#end connect

#main
if __name__ == "__main__":
	IRCconnect(server, port, nick)
	irc.join(channel)
	server_to_irc = linkToIRC(IRCSock)
	irc_to_server = linkFromIRC(IRCSock)
	server_to_irc.start()
	irc_to_server.start()
#end main
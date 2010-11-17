import socket, string
import irc

chan = "#wwu-dcpp"

class IRCBot(object):
	"""IRC Bot"""
	# IRC parameters
	server = "irc.freenode.net"
	port = 6667
	nick = "mrpersonLinker"
	channel = chan
	IRCSock = socket.socket()

	# linking server paprameters
	localServer = "localhost"
	localPort = 7013
	address = (localServer, localPort)
	UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	loggedOn = False

	def read(self):
		print "in irc bot read\n"
		buff = ""
		try:
			buff += self.IRCSock.recv(1024)
			return buff
		except socket.error, msg:
			return

		return buff
	# end read
	
	def IRCconnect(self, server, port, nick):
		ident = nick
		host = nick
		realname = nick
		
		self.IRCSock.connect((server, port))
		irc.serverMessage("NICK %s" % nick)
		irc.serverMessage("USER %s %s bla :%s" % (ident, host, realname))
		
		return True
	#end connect

	def parse(self, message):
		print "in irc bot parse\n"
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
		self.IRCconnect(self.server, self.port, self.nick)
		self.UDPSock.connect(self.address)
		irc.join(self.channel)
		while True:
			self.parse(self.read())
	#end run
#end IRCBot

# main
bot = IRCBot()
irc.s = IRCBot.IRCSock

bot.run()
#end main

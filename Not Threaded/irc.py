s = "some socket" # assign from main program; ex: irc.s = s = socket.socket()

def message(chan, message):
	s.send("PRIVMSG "+chan+" :"+message+"\r\n")
	print "PRIVMSG "+chan+" :"+message+"\r\n"

	return True
# end message

def PM(user, message):
	s.send("PRIVMSG "+user+" :"+message+"\r\n")
	#s.send("PRIVMSG %s :%s\r\n" % (user, message))
	print "PRIVMSG "+user+" :"+message+"\r\n"
	
	return True
# end PM

def serverMessage(message):
	s.send(message+"\r\n")
	print message+"\r\n"

	return True
# end serverMessage

def join(chan):
	serverMessage("JOIN %s" % chan)

	return True
# end join

def leave(chan):
	serverMessage("PART %s" % CHANNEL)

	return True
# end leave

def linkParse(line):
	if line[0][0] == ':':
		line[0] = line[0][1:len(line[0])]
		message = ""
#		for i in 0..len(line[0]):
#			if line[0][i] != '!':
#				message += line[0][i]
#			else:
#				i = len(line[0])+10
		count = 0
		for word in line:
			if count > 2:
				message += word+' '
			count +=1

		return message
	return None	
# end linkParse

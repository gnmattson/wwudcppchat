import thread
import socket, string

class linkServ(object):
	"""A chat linking server"""
	recv_conn = socket.socket()
	send_conn = socket.socket()
	def __init__(self, recv_connection, send_connection):
		recv_conn = recv_connection
		send_conn = send_connection

	def read(self):
		buffer = ""
		try:
			buffer += self.recv_conn.recv(1024)
			return buffer
		except socket.error, msg:
			return

		return buffer
	# end read
    
	def parse(self, message):
		# the only way parse() is executed without message == TYPE none is
		# when UDPSock.recv() tries to read a message that's too big
		if not message:
			print "last message was too long to link"
			#self.UDPSock.sendto("!dcpp**last message was too long to link**", self.address)
			#self.UDPSock.sendto("!irc**last message was too long to link**", self.address)
			return

		print message

		# uncomment code when you find out how to send to clients
		#if message[0:7] == "**IRC**":
		#   self.outUDPSock.sendto("!dcpp"+message[7:len(message)], self.outAddress)
		#elif message[0:8] == "**DCPP**":
		#   self.outUDPSock.sendto("!irc"+message[8:len(message)], self.outAddress)

		return True
	# end parse

	def send(self, message):
		self.send_conn.send(message)

	def run(self):
		print "one process in run"
		while True:
			message = self.read()
			if self.parse(message):
				self.send(message)
	# end run
    
# end linkServ

# main
#initialize the irc socket
irc_server = "localhost"
irc_port = 7010
irc_address = (irc_server, irc_port)
irc_UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
irc_UDPSock.bind(irc_address)
#initialize the dcpp socket
dcpp_server = "localhost"
dcpp_port = 7011
dcpp_address = (dcpp_server, dcpp_port)
dcpp_UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dcpp_UDPSock.bind(dcpp_address)
if __name__ == '__main__':
	dc_to_irc_linker = linkServ(dcpp_UDPSock, irc_UDPSock)
	
	#irc_to_dc_linker = linkServ(irc_UDPSock, dcpp_UDPSock)
	print "creating dc to irc linker process"
	dc = Process(target=dc_to_irc_linker.run)
	#print "creating irc to dc linker process"
	#irc = Process(target=irc_to_dc_linker.run)
	print "starting dc process"
	dc.start()
	#print "starting irc process"
	#irc.start()
	print "after dc process starts"
	#dc.join()
	#irc.join()
	#print "end of program"
irc_to_dc_linker = linkServ(irc_UDPSock, dcpp_UDPSock)
print "running irc linker in main process"
irc_to_dc_linker.run()
foo = input('press enter to end program')
# end main


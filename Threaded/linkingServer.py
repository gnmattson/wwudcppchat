from threading import Thread
import socket, string

class linkServ(Thread):
	"""A threaded chat linking server"""
	def __init__(self, recv_connection, send_connection, send_address, debug):
		Thread.__init__(self)
		self.recv_conn = recv_connection
		self.send_conn = send_connection
		self.send_addr = send_address
		self.debug_id = debug
		print "\n in init for " + str(self.debug_id) + " recv = " + str(self.recv_conn.getsockname()) + " send = " + str(self.send_conn.getsockname())
		
	def read(self):
		print "\n in read in "+self.debug_id
		buffer = ""
		try:
			buffer += self.recv_conn.recv(1024)
			return buffer
		except socket.error, msg:
			return
	#end read
	
	#not currently used for anything, can be removed
	def parse(self, message):
		print "\n in parse in "+self.debug_id
		# the only way parse() is executed without message == TYPE none is
		# when UDPSock.recv() tries to read a message that's too big
		if not message:
			print "\n last message was too long to link"
			return False

		print message
		return True
	# end parse
	
	#when using sendto the message is not received by the bots
	#when using send an exception is raised
	def send(self, message):
		print "\n in send in "+self.debug_id
		try:
			self.send_conn.sendto(message, self.send_addr)
		except:
			print "you fail at sending\n"
			pass
		
	def run(self):
		print "\n in run in "+self.debug_id
		
		while True:
			message = ""
			message = self.read()
			print "\n message read in "+self.debug_id
			if not message:
				print "message was too long to link\n"
			else:
				print message
				self.send(message)
	#end run
	
#end linkServ

#main
#initialize the irc sockets
irc_server = "localhost"
irc_send_port = 7012
irc_recv_port = 7013
irc_send_address = (irc_server, irc_send_port)
irc_recv_address = (irc_server, irc_recv_port)
irc_send_UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
irc_recv_UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
irc_send_UDPSock.bind(irc_send_address)
irc_recv_UDPSock.bind(irc_recv_address)
print "\n string representation of irc sockets "+str(irc_send_UDPSock.getsockname())+" "+str(irc_recv_UDPSock.getsockname())

#initialize the dcpp sockets
dcpp_server = "localhost"
dcpp_send_port = 7014
dcpp_recv_port = 7015
dcpp_send_address = (dcpp_server, dcpp_send_port)
dcpp_recv_address = (dcpp_server, dcpp_recv_port)
dcpp_send_UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dcpp_recv_UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dcpp_send_UDPSock.bind(dcpp_send_address)
dcpp_recv_UDPSock.bind(dcpp_recv_address)
print "\n string representation of dcpp sockets "+str(dcpp_send_UDPSock.getsockname())+" "+str(dcpp_recv_UDPSock.getsockname())

if __name__ == "__main__":
	dc_to_irc_link = linkServ(dcpp_recv_UDPSock, irc_send_UDPSock, irc_send_address, "dc_to_irc")
	irc_to_dc_link = linkServ(irc_recv_UDPSock, dcpp_send_UDPSock, dcpp_send_address, "irc_to_dc")
	print "starting threads"
	dc_to_irc_link.start()
	irc_to_dc_link.start()
	try:
		input("hit enter to continue")
	except:
		pass
	dcpp_send_UDPSock.close()
	dcpp_recv_UDPSock.close()
	irc_send_UDPSock.close()
	irc_recv_UDPSock.close()
	exit()
#end main

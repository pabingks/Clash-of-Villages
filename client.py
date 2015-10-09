import socket, select, string, sys
import Queue
import threading

class Client():
	def __init__(self, queue):
		self.queue = queue

		self.connected = False
		self.host = '192.168.0.18'
		self.port = 5000

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.settimeout(2)


	def connectToChatServer(self):
		notConnected = True
		attempts = 0
		while (notConnected and attempts < 10):
			try :
				self.s.connect((self.host, self.port))
				self.connected = True
				notConnected = False
				self.connection()
			except :
				print 'Unable to connect'
				attempts = attempts + 1


	def connection(self):
		while 1:
			socket_list = [sys.stdin, self.s]

			# Get the list sockets which are readable
			read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
			
			for sock in read_sockets:
				#incoming message from remote server
				print("huehueue")
				if sock == self.s:
					data = sock.recv(4096)
					if not data :
						print '\nDisconnected from chat server'
						#need to catch if disconnected from chat server
						sys.exit()
					else :
						self.queue.put(data)
				else:
					print "sdfsdf"


	def sendMessage(self, msg):
		self.s.send(msg)



if __name__ == "__main__":
	queue = Queue.Queue()
	client = Client(queue)
	threading.Thread(target=client.connectToChatServer, args=()).start()
from Tkinter import *
import threading
import socket, select, string, sys
import client
import Queue

class COVWindow(Frame):
	def __init__(self, root, height, width):
		Frame.__init__(self, root)
		self.screen_width = width
		self.screen_height = height
		self.pack()
		self.create_widgets()
		self.checkChatQueue()

	def create_widgets(self):
		self.leftWindow = Frame(self, width=(self.screen_width*0.25), height=self.screen_height, bg = "red")
		self.leftWindow.pack(side=LEFT)

		self.rightWindow = Frame(self, width=(self.screen_width*0.75), height=self.screen_height, bg = "yellow")
		self.rightWindow.pack()

		self.chatWindow = Frame(self.leftWindow, width=(self.screen_width*0.25), height=(self.screen_height*0.92), bg  =  "blue")
		self.chatWindow.pack(side=TOP, fill=X)


		self.statusWindow = PanedWindow(self.leftWindow, width=(self.screen_width*0.25), height=(self.screen_height*0.08), bg = "green")
		self.statusWindow.pack()

		self.chatAreaFrame = Frame(self.chatWindow, width=(self.screen_width*0.25), height=(self.screen_height*0.9))
		self.chatAreaFrame.pack_propagate(False)
		self.chatAreaFrame.pack(side=TOP)

		self.chatScrollbar = Scrollbar(self.chatAreaFrame)
		self.chatScrollbar.pack(side=RIGHT, fill=Y)

		self.chatArea = Text(self.chatAreaFrame, wrap = WORD, bd = 2, padx = 5, pady = 5, spacing3 = 10, yscrollcommand=self.chatScrollbar.set) 
		self.chatArea.pack(expand = YES, fill = BOTH, side = LEFT)
		self.chatArea.config(state="disabled")

		self.chatScrollbar.config(command=self.chatArea.yview)

		self.chatBox = Entry(self.chatWindow, bd = 3)
		self.chatBox.pack(side=LEFT, expand=YES, fill=BOTH)

		self.sendButton = Button(self.chatWindow, text = "Send", command=self.sendChat)
		self.sendButton.pack(side=LEFT)

	def sendChat(self):
		text = self.chatBox.get()
		text = text.strip(' \t\n\r')
		if text != '':
			global client
			# self.chatArea.config(state="normal")
			# self.chatArea.insert(END, text + "\n")
			# self.chatArea.config(state="disabled")
			# client.sendChat(client.s, text)
			client.sendMessage(text)
		self.chatBox.delete(0, 'end')


	def checkChatQueue(self):
		global client
		try:
			msg = client.queue.get(0)
			self.chatArea.config(state="normal")
			self.chatArea.insert(END, msg + "\n")
			self.chatArea.config(state="disabled")
		except Queue.Empty:
			pass
		self.chatArea.after(50, self.checkChatQueue)
		
 

def main():
	root = Tk()
	global client

	client = c.Client(Queue.Queue())
	clientThread = threading.Thread(target = client.connectToChatServer, args =())
	clientThread.daemon = True
	clientThread.start()
	
	root.title('CMSC 137 CD-2L Team Zen: Clash of Villages')
	cov = COVWindow(root, root.winfo_screenheight(), root.winfo_screenwidth())
	root.mainloop()

if __name__ == '__main__':
	client = None
	main()

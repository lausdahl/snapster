import NeighbourList
import Node
import socket
from threading import Thread
from List import List
from SharedFolder import SharedFolder
from Settings import Settings
import select
import sys
from SharedItem import SharedItem
class FileShareServer(Thread):
    currentNode = None
    
    def __init__(self, me=Node):
        Thread.__init__(self)
        self.currentNode = me
        self.terminateServer = 0
        self.s = None
        self.client = None
        self.elements=None
    
    def run(self):
        self.__RecieveMessage()
        
    def StopServer(self):
        self.terminateServer = 1
        if (self.s is not None):
            self.s.close()
        #self._Thread__stop()
    
    def __RecieveMessage(self):
        backlog = 5
        size = 1024
        data = ""
        address = socket.gethostbyname(socket.gethostname())
        #try:
        print "Server fileshare starting on " + self.currentNode.ip + ":" + str(self.currentNode.fileSharePort)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', self.currentNode.fileSharePort))
        self.s.listen(backlog)
        #self.s.setblocking(0)
        while self.terminateServer==0:
            resetSocket = False
            (rd, wr, ex) = select.select([self.s], [], [], 2.0)
            #print (rd, wr, ex)
            if (len(rd) > 0 and self.terminateServer == 0):
                self.client, address = self.s.accept()
                data = self.client.recv(size)
                
                self.elements = str(data).split('|')
                if (len(self.elements) == 0):
                    print "Unknown message: " + str(data)
                else:
                    message = str(self.elements[0])
                    if (message == "Download"):
                        self.__HandleDownloadFile()
                    else:
                        self.__HandleUnknownMessage(message)
                self.client.close()
            else:
                resetSocket = True
            
            if (resetSocket):
                self.s.close()
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind(('', self.currentNode.fileSharePort))
                self.s.listen(backlog)
        self.s.close()
        print "Server stopped"
    def __HandleDownloadFile(self,item):
        file=SharedFolder.GetSharedFileInfo(item)
        f = open(fileName, "rb")
        data = f.read()
        f.close()
        
        self.client.send(data)
        self.client.close()

#!/usr/bin/env python

import NeighbourList
import Node
import socket
from threading import Thread
from List import List
from SharedFolder import SharedFolder
from Settings import Settings
import select
import sys
import os
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
        while self.terminateServer==0:
            resetSocket = False
            (rd, wr, ex) = select.select([self.s], [], [], 2.0)
            if (len(rd) > 0 and self.terminateServer == 0):
                try:
                    #print "ShareServer, Client connected"
                    self.client, address = self.s.accept()
                    data = self.client.recv(size)
                    #print "ShareServer, data: " + data
                    
                    self.elements = str(data).split('|')
                    if (len(self.elements) > 0):
                        message = str(self.elements[0])
                        if (message == "Download"):
                            self.__HandleDownloadFile(self.elements[1])
                    self.client.close()
                except socket.error:
                    resetSocket = True
            else:
                pass#print "ShareServer, no connection"
            
            if (resetSocket):
                self.s.close()
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind(('', self.currentNode.fileSharePort))
                self.s.listen(backlog)
        self.s.close()
        print "Server stopped"
        
    def __HandleDownloadFile(self,fileName):
        file = Settings().SharingFolderPath + "\\" + fileName
        if (os.path.exists(file)):
            f = open(file, "rb")
            data = f.read()
            #while 1:
            #    data = f.read(1024)
            #    if (len(data) > 0):
            #        sent = s.send(data[totalsent:])
            #        if sent == 0:
            #            break
            #    else:
            #        break
            f.close()
            self.client.send(data)

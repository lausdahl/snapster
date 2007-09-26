#!/usr/bin/env python

import NeighbourList
import Node
import socket
from threading import Thread
from List import List
from SharedFolder import SharedFolder
from SharedItem import SharedItem
from Settings import Settings
from FileShareServer import FileShareServer
from DownloadItem import DownloadItem
from DownloadList import DownloadList
import select
import sys
import random

class Server(Thread):
    currentNode = None
    NODE_LENGTH=6
    
    def __init__(self, me=Node):
        Thread.__init__(self)
        self.currentNode = me
        self.terminateServer = 0
        self.s = None
        self.client = None
	self.list = List()
        self.neighbourList = NeighbourList.NeighbourList()
        self.elements = None
        self.FileServer = None
    
    def run(self):
        self.FileServer = FileShareServer(self.currentNode)
        self.FileServer.start()
        self.__RecieveMessage()
       
        
    def StopServer(self):
        self.terminateServer = 1
        self.FileServer.StopServer()
	self.FileServer.join()
        
        if (self.s is not None):
            self.s.close()
        #self._Thread__stop()
    
    def __RecieveMessage(self):
        backlog = 5
        size = 1024
        data = ""
        address = socket.gethostbyname(socket.gethostname())
        #try:
        print "Server starting on " + self.currentNode.ip + ":" + str(self.currentNode.port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', self.currentNode.port))
        self.s.listen(backlog)
        #self.s.setblocking(0)
        while self.terminateServer==0:
            resetSocket = False
            (rd, wr, ex) = select.select([self.s], [], [], 2.0)
            #print (rd, wr, ex)
            if (len(rd) > 0 and self.terminateServer == 0):
                self.client, address = self.s.accept()
                data = self.client.recv(size)
                #print "Client connected from " + str(address)
                #print "__RecieveMessage, Message recieved: " + str(data)
                self.elements = str(data).split('|')
                if (len(self.elements) == 0):
                    print "Unknown message: " + str(data)
                else:
                    message = str(self.elements[0])
                    if (message == "ping"):
                        self.__HandlePing()
                    elif (message == "Request"):
                        self.__HandleNeighbourRequest()
                    elif (message == "Drop"):
                        self.__HandleNeighbourDrop()
                    elif (message == "areYouAwake"):
                        self.__HandleAwakeRespone()
                    elif (message == "Query"):
                        self.__HandleQuery()
                    elif ( message == "QueryHit"):
                        self.__HandleQueryHit(data)
                    else:
                        self.__HandleUnknownMessage(message)
                self.client.close()
            
            if (resetSocket):
                self.s.close()
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind(('', self.currentNode.port))
                self.s.listen(backlog)
	#print "Closing socket in server"
	try:
	    self.client.close()
	    self.s.shutdown(2)
	except:
	    pass
        self.s.close()
	#print "Server: socket: " + str(self.s)
        print "Server stopped"
                
    def __HandlePing(self):
        #print "Ping recieved"
        
        #add node to list
        message = ""
        for i in range(0,self.NODE_LENGTH):
            message = message + str(self.elements[i+1]) + "|"
        message = message[:-1]
            
        newNode = Node.Node()
        if (not newNode.SetNodeFromMessage(message)):
            return
        List().AddNode(newNode)
        
        totalsent = 0
	neighbourMessage = self.neighbourList.ToMessage()
	listMessage = self.list.ToMessage()
	message = ""
        if (len(listMessage) > 0):
		message = listMessage
	if (len(neighbourMessage) > 0):
		if (len(message) > 0):
			message += ";"
		message += neighbourMessage
        #print "__HandlePing, Answering with: " + str(message)
        try:
            while totalsent < len(message):
                sent = self.client.send(message[totalsent:])
                if sent == 0:
                    raise RuntimeError, "socket connection broken"
                totalsent = totalsent + sent
        except socket.error:
            #print('Send failed')
	    pass
        self.client.close()
            
    def __HandleNeighbourRequest(self):
        if(len(self.elements) < self.NODE_LENGTH):
            print "Error no guid recieved as a node"
            return

        message = ""
        for i in range(0,self.NODE_LENGTH):
            message=message+str(self.elements[i+1])+"|"
        message = message[:-1]
            
        newNode = Node.Node()
        newNode.SetNodeFromMessage(message)
        #print "__HandleNeighbourRequest, Message: " + str(message)
        acceptAsNeighbour = False
        
        if (self.neighbourList.Contains(newNode)):
            # already there
            acceptAsNeighbour = True
            #print "__HandleNeighbourRequest, Friend already exists: " + str(newNode.ip)
        elif (not self.neighbourList.IsFull()):
            #we have room
            self.neighbourList.Add(newNode)
            #print "__HandleNeighbourRequest, Added new friend: " + str(newNode.ip)
            acceptAsNeighbour = True
        else:
            #We have not room, so find a node to drop
            nodeToDrop = Node.Node()
            nodeToDrop.quality = 0
            nodeWithMaxQuality = Node.Node()
            nodeWithMaxQuality.quality = 0
            for node in self.neighbourList.GetAll():
                if (node.quality >= newNode.quality and node.quality > nodeToDrop.quality):
                    nodeToDrop = node
                if (nodeWithMaxQuality.quality < node.quality):
                    nodeWithMaxQuality = node
                    
            if(nodeToDrop.quality > 0 and
               (nodeWithMaxQuality.quality < newNode.quality or self.neighbourList.Count() > newNode.numberOfNeighbours)):
                self.DropNode(nodeToDrop)
                self.neighbourList.Remove(nodeToDrop)
                self.neighbourList.Add(newNode)
                #print "__HandleNeighbourRequest, Added new friend: " + str(newNode.ip) + " in stead of: " + str(nodeToDrop.ip)
                acceptAsNeighbour = True
	
	self.list.AddNode(newNode)
        if(acceptAsNeighbour):
            self.client.send("YES|" + str(self.currentNode.ToMessage()))
        else:
            self.client.send("NO")
            
    def DropNode(self, nodeToDrop):
        if (nodeToDrop is None):
            return
        
        dropSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            dropSocket.connect((nodeToDrop.ip, nodeToDrop.port))
            totalsent = 0
            message = "Drop|" + str(self.currentNode.ToMessage())
            while totalsent < len(message):
                sent = dropSocket.send(message[totalsent:])
                if sent == 0:
                    break#raise RuntimeError, "socket connection broken"
                totalsent = totalsent + sent
            dropSocket.close()
        except socket.error:
            pass
            #print('Error in drop socket')

    def __HandleNeighbourDrop(self):
        if(len(self.elements) < self.NODE_LENGTH):
            print "Error no guid recieved as a node"
            return
        
        message=''
        for i in range(0,self.NODE_LENGTH):
            message=message+str(self.elements[i+1])+"|"
        message = message[:-1]
            
        node = Node.Node()
        node.SetNodeFromMessage(message)
        self.neighbourList.Remove(node)
	self.list.AddNode(node)
        #print "Droped neighbour: " + node.id
    
    def __HandleAwakeRespone(self):
        #Return the number of currentConnected neightbours
        count = str(self.neighbourList.Count())
	#print "__HandleAwakeResponse, #neighbours: " + count
        self.client.send("YES," + count)
    
    def __HandleUnknownMessage(self, message):
        pass
        #print "Unknown message from client: " + str(message)
        
    def __HandleQuery(self):
	#print "__HandleQuery, self.elements: " + str(self.elements)
        if(len(self.elements) < self.NODE_LENGTH):
            print "Error no guid recieved as a node"
            return
        
        message = ""
        key = str(self.elements[1])
        Ttl = int(self.elements[2])-1
        for i in range(0,self.NODE_LENGTH):
            message = message + str(self.elements[i+3]) + "|"
        message = message[:-1]
	
	self.elements[2] = str(Ttl)
	forwardMessage = ""
        for s in self.elements:
            forwardMessage += s + "|"
        forwardMessage = forwardMessage[:-1]
        
        queryRequestNode = Node.Node()
        queryRequestNode.SetNodeFromMessage(message)
	self.list.AddNode(queryRequestNode)
        
        #print query
        #print "\nRecieved query: " + key + ", from: " + self.elements[3]
        #print "__HandleQuery, Ttl: " + str(Ttl)
        
        #first vi search
        s = Settings()
        path = s.SharingFolderPath
        sharedFolder = SharedFolder(path)
	#print "__HandleQuery, path: " + path
        if(sharedFolder.Contains(key)):
            print "\nFound query locally, sending query hit"
            self.__SendQueryHit(key, queryRequestNode)
	else:
		print "\nCould not find query '" + key + "' here"
        if(Ttl > 0):
            self.__ForwardQuery(forwardMessage, queryRequestNode)
        
    def __SendQueryHit(self, key, reciever):
        #print "\nSending queryHit on '" + key + "', to '" + str(reciever.ip) + "'"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        #connect to node
        try:
            #print "__SendQueryHit, Connecting to: " + str(reciever.ip) + ":" + str(reciever.port)
            s.connect((reciever.ip, reciever.port))
            totalsent = 0
            
            sf = SharedFolder(Settings().SharingFolderPath)
            fileList = sf.GetSharedFiles(key)
            
            message = "QueryHit|" + str(key) + "|" + str(Settings().GetAppNode().ToMessage()) + "&"
            counter = 0
            for si in fileList:
                if (counter > 0):
                    message = message + "|"
                message = message + si.ToMessage()
                counter = counter + 1
            #print "__SendQueryHit, message: " + message
            
            try:
                while totalsent < len(message):
                    sent = s.send(message[totalsent:])
                    if sent == 0:
                        raise RuntimeError, "socket connection broken"
                    totalsent = totalsent + sent
            except socket.error:
                pass
                #print('__SendQueryHit, Send failed')
        except socket.error:
            pass
            #print('__SendQueryHit, Cannot connect to: ' + str(reciever.ip))
        s.close()
            
    def __ForwardQuery(self, message, senderNode):
        for n in self.__FindKWalkers(senderNode):
            self.__SendQuery(message,n)
            
    def __FindKWalkers(self, senderNode):
        kwCount = Settings().NumberOfKWalkers
        count = 0
        kWalker = []
        for n in self.neighbourList.GetAll():
            if (str(n.id) == str(senderNode.id)):
                continue
            if(count <= kwCount):
		#print "Adding node " + n.ip + " to kWalker list"
                kWalker.append(n)
                count = count + 1
        return kWalker
    
    def __SendQuery(self,message,reciever):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        #connect to node
        try:
            #print "ForwardQuery, Connecting to: " + str(reciever.ip) + ":" + str(reciever.port) + ", message: " + message
            s.connect((reciever.ip, reciever.port))
            totalsent = 0
            while totalsent < len(message):
                sent = s.send(message[totalsent:])
                if sent == 0:
                    raise RuntimeError, "socket connection broken"
                totalsent = totalsent + sent
	    #print "Forwardquery delivered"
        except:
            #print('ForwardQuery, Cannot connect to: ' + str(reciever.ip))
	    pass
        s.close()
            
    def __HandleQueryHit(self, message):
        elements = message.split('&')
        nodeInfo = elements[0].split('|')
        fileList = elements[1]

        keyword = nodeInfo[1]
        message = ""
        for i in range(0,self.NODE_LENGTH):
            message = message + str(nodeInfo[i+2]) + "|"
        message = message[:-1]
        
        host = Node.Node()
        host.SetNodeFromMessage(message)
        #host.Show()
        
        files = fileList.split('|')
        #print "__HandleQueryHit, Filelist: " + str(fileList)
        #print "__HandleQueryHit, Files: " + str(files)
        
        dl = DownloadList()
        for file in files:
            si = SharedItem()
            si.SetFromMessage(file)
            di = DownloadItem()
            di.SetKeyword(keyword)
            di.SetFilename(si.Name())
            di.SetRelevance(si.Relevance())
            di.SetSize(si.Size())
            di.SetIp(host.ip)
            di.SetPeer(host.id)
            di.SetPort(host.fileSharePort)
            di.SetId(random.randint(0, 20000))
            dl.Add(di)
    
        
        
        
        
        
        
        

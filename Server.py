import NeighbourList
import Node
import socket
from threading import Thread
from List import List
from SharedFolder import SharedFolder
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
                #print "Message recieved: " + str(data)
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
            else:
                resetSocket = True
            
            if (resetSocket):
                self.s.close()
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind(('', self.currentNode.port))
                self.s.listen(backlog)
        self.s.close()
        print "Server stopped"
                
    def __HandlePing(self):
        #print "Ping recieved"
        totalsent = 0
        message = List().ToMessage()
        #print "Answering with: " + str(message)
        try:
            while totalsent < len(message):
                sent = self.client.send(message[totalsent:])
                if sent == 0:
                    raise RuntimeError, "socket connection broken"
                totalsent = totalsent + sent
        except socket.error:
            print('Send failed')
        self.client.close()
            
    def __HandleNeighbourRequest(self):
        
        if(len(self.elements)<self.NODE_LENGTH):
            print "Error no guid recieved as a node"
        message=''
        for i in range(0,self.NODE_LENGTH):
            message=message+str(self.elements[i+1])+"|"
        message = message[:-1]
            
        newNode = Node.Node()
        newNode.SetNodeFromMessage(message)
        #print "Message: " + str(message)
        acceptAsNeighbour = False
        
        if (self.neighbourList.Contains(newNode)):
            # already there
            acceptAsNeighbour = True
            #print "Friend already exists: " + str(newNode.ip)
        elif (not self.neighbourList.IsFull()):
            #we have room
            self.neighbourList.Add(newNode)
            #print "Added new friend: " + str(newNode.ip)
            acceptAsNeighbour = True
        else:
            #We have not room, so find a node to drop
            nodeToDrop = Node.Node()
            nodeToDrop.quality = 0
            nodeWithMaxQuality = Node.Node()
            nodeWithMaxQuality = 0
            for node in self.neighbourList.GetAll():
                if (node.quality >= newNode.quality and node.quality > nodeToDrop.quality):
                    nodeToDrop = node
                if (nodeWithMaxQuality.quality < node.quality):
                    nodeWithMaxQuality = node
                    
            if(nodeToDrop.quality > 0 and
               (nodeWithMaxQuality.quality < newNode.quality or self.neighbourList.count > newNode.numberOfNeighbours)):
                dropSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    dropSocket.connect((nodeToDrop.ip, nodeToDrop.port))
                    totalsent = 0
                    message = "Drop|" + str(self.currentNode.ToMessage())
                    try:
                        while totalsent < len(message):
                            sent = dropSocket.send(message[totalsent:])
                            if sent == 0:
                                raise RuntimeError, "socket connection broken"
                            totalsent = totalsent + sent
                        dropSocket.close()
                    except socket.error:
                        print('Error in dropsocket in send')
                except socket.error:
                    print('Error in drop socket')
                self.neighbourList.Remove(nodeToDrop)
                self.neighbourList.Add(newNode)
                #print "Added new friend: " + str(newNode.ip) + " in stead of: " + str(nodeToDrop.ip)
                acceptAsNeighbour=True
                
        if(acceptAsNeighbour):
            self.client.send("YES|"+str(self.currentNode.ToMessage()))
        else:
            self.client.send("NO")

    def __HandleNeighbourDrop(self):
        self.neighbourList = NeighbourList.NeighbourList()
        if(len(self.elements) < self.NODE_LENGTH):
            print "Error no guid recieved as a node"
        message=''
        for i in range(0,self.NODE_LENGTH):
            message=message+str(self.elements[i+1])+"|"
        message = message[:-1]
            
        node = Node.Node()
        node.SetNodeFromMessage(message)
        self.neighbourList.Remove(node)
        #print "Droped neighbour: " + node.id
    
    def __HandleAwakeRespone(self):
        #Return the number of currentConnected neightbours
        count = str(self.neighbourList.Count())
        self.client.send("YES,"+ count)
    
    def __HandleUnknownMessage(self, message):
        pass
        #print "Unknown message from client: " + str(message)
        
    def __HandleQuery(self):
        if(len(self.elements)<self.NODE_LENGTH):
            print "Error no guid recieved as a node"
        message = ''
        key = str(self.elements[1])
        Ttl = int(self.elements[2])-1
        for i in range(0,self.NODE_LENGTH):
            message = message + str(self.elements[i+3]) + "|"
        message = message[:-1]
            
        queryRequestNode = Node.Node()
        queryRequestNode.SetNodeFromMessage(message)
        
        #print query
        print "\nRecieved query: " + key + ", from: " + self.elements[3]
        #print "__HandleQuery, self.elements[3]: " + self.elements[3]
        
        #first vi search
        #path = sys.path[0] + "\\Files"
        s = Settings()
        path = s.SharingFolderPath
        sharedFolder = SharedFolder(path)
        if(sharedFolder.Contains(key)):
            print "\nFound query locally, sending query hit"
            self.__SendQueryHit(key, queryRequestNode)
        if(Ttl >= 0):
            self.__ForwardQuery(message, queryRequestNode)
        
    def __SendQueryHit(self, key, reciever):
        print "\nForwarding query '" + key + "', to '" + str(reciever.ip) + "'"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        #connect to node
        try:
            #print "__SendQueryHit, Connecting to: " + str(reciever.ip) + ":" + str(reciever.port)
            s.connect((reciever.ip, reciever.port))
            totalsent = 0
            settings = Settings()
            path = settings.SharingFolderPath
            sf = SharedFolder(path)
            si = sf.GetSharedFileInfo(key)
            message = "QueryHit|" + str(key) + "|" + str(Settings().GetAppNode().ToMessage())+"&"+str(si.Name())+"|"+str(si.Size())
            #print "SendQueryhit: Sending: " + message
            try:
                while totalsent < len(message):
                    sent = s.send(message[totalsent:])
                    if sent == 0:
                        raise RuntimeError, "socket connection broken"
                    totalsent = totalsent + sent
            except socket.error:
                print('__SendQueryHit, Send failed')
        except socket.error:
            print('__SendQueryHit, Cannot connect to: ' + str(reciever.ip))
        s.close()
            
    def __ForwardQuery(self, message, senderNode):
        for n in self.__FindKWalkers(senderNode):
            self.__SendQuery(message,n)
            
    def __FindKWalkers(self, senderNode):
        kwCount = Settings().NumberOfKWalkers
        count = 0
        kWalker = []
        for n in NeighbourList.NeighbourList().GetAll():
            if (n.id == senderNode.id):
                continue
            if(count <= kwCount):
                kWalker.append(n)
                count = count + 1
        return kWalker
    
    def __SendQuery(self,message,reciever):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        #connect to node
        try:
            #print "ForwardQuery, Connecting to: " + str(reciever.ip) + ":" + str(reciever.port)
            s.connect((reciever.ip, reciever.port))
            totalsent = 0
            #message="Query|key|"+str(sender.ToMessage())
            try:
                while totalsent < len(message):
                    sent = s.send(message[totalsent:])
                    if sent == 0:
                        raise RuntimeError, "socket connection broken"
                    totalsent = totalsent + sent
            except socket.error:
                print('ForwardQuery, Send failed')
            s.close()
        except socket.error:
            print('ForwardQuery, Cannot connect to: ' + str(reciever.ip))
            
    def __HandleQueryHit(self, message):
        elements = message.split('&')
        nodeInfo = elements[0]
        fileList = elements[1]
        
        nodeElements = nodeInfo.split('|')
        keyword = str(nodeElements[1])
        ip = str(nodeElements[2])
        sharePort = int(nodeElements[3])
        peer = str(nodeElements[4])
        
        files = fileList.split('|')
        fileName = files[0]
        fileSize = files[1]
        print "__HandleQueryHit, fileList: " + fileList
        
        dl = DownloadList()
        di = DownloadItem()
        di.SetKeyword(keyword)
        di.SetFilename(fileName)
        di.SetIp(ip)
        di.SetPeer(peer)
        di.SetPort(sharePort)
        di.SetId(random.randint(0, 200000))

        dl.append(di)
        
        #print "\nFound '" + str(elements[1]) + "', at: '" + str(elements[2]) + "'"
        
        
        
        
        
        
        
        
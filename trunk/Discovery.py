#!/usr/bin/env python

import time
import Node
from Settings import Settings
import NeighbourList
import List
import socket
from threading import Thread
from Settings import Settings

class Discovery(Thread):
    NODE_LENGTH = 6
    
    def __init__(self,node=None):
        Thread.__init__(self)
        self.stopRun = False
        self.neighbourList = NeighbourList.NeighbourList()
        self.list = List.List()
        self.nodeMe=node
        self.s=Settings()
    
    def Stop(self):
        self.stopRun = True
        
    def run(self):
        print "Discovery starting..."
        print "Finding peers"
        self.__FindPeers()
        print "Done bootstrapping"
        #print "Peer searching ended"
        while(not self.stopRun):
            #print "Check neighbours"
            self.__CheckNeighbours()
            #print "Finding neighbours"
            self.__FindNeighbours()
            #print "Neighbour searching ended"
            #print "Neighbour isAlive ended"
            time.sleep(self.s.rediscovery_delay_ms/1000)
        print "Discovery ended"
        
    def __FindPeers(self):
        nodeList = Settings().GetBootStrapNodes()#self.list.GetNodes()
        #print "__FindPeers, nodeList: " + str(nodeList)
        self.list.Clear()
        for node in nodeList:
            #print "__FindPeers, finding node: " + node.ToString()
            if (self.stopRun):
                return
            if (self.__Ping(node)):
                self.list.AddNode(node)
        
    def __Ping(self, node=Node):
        returnValue = False
        #create an INET, STREAMing socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        #print "Ping, Try to connect to node: " + str(node.ip) + " on port: " + str(node.port)
        try:
            s.connect((node.ip, node.port))
            #print "Connected"
            totalsent = 0
            message = "ping|" + str(self.nodeMe.ToMessage())
            #print ('Ping, Client sending ping to ' + str(node.ip))
            try:
                while totalsent < len(message):
                    sent = s.send(message[totalsent:])
                    if sent == 0:
                        raise RuntimeError, "socket connection broken"
                    totalsent = totalsent + sent
                
                size = 1024
                data = ""
                while 1:
                    chunk = s.recv(size)
                    if (not chunk):
                        break
                    data = data + chunk
                if (len(str(data)) > 0):
                    List.List().SetListFromMessage(str(data))
                returnValue = True
            except socket.error:
                #print('Ping, Recieve failed')
                returnValue = False
            s.close()
        except socket.error:
            #print('Ping, Cannot connect')
            returnValue = False
        return returnValue
    
    def __FindNeighbours(self):
        nodeList = self.list.GetNodes()
        #print "__FindNeighbours, nodeList: " + str(nodeList)
        if (nodeList is None):
            return
        
        #print "__FindNeighbours, Finding neighbours"
        for node in nodeList:
            if (self.stopRun):
                return
            
            #do wi want this node as a friend
            
            #test for full list
            if (self.neighbourList.IsFull()):
                return
            
            #test if node is not already in neighbour list
            if (not self.neighbourList.Contains(node)):
                self.__RequestToBeNeighbours(node)#):#we have room and handle agreement
                
    def __DropNode(self, node):
        self.neighbourList.Remove(node)
        totalsent = 0
        message = "Drop|" + str(node.ToMessage())
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((node.ip, node.port))
            while totalsent < len(message):
                sent = s.send(message[totalsent:])
                if sent == 0:
                    raise RuntimeError, "socket connection broken"
                totalsent = totalsent + sent
        except socket.error:
            print 'Error in send drop'
        s.close()
        #send drop cmd to node to be removed from its neighbour list, or just du not response at next AreYouThere=NO
    
    def __RequestToBeNeighbours(self, node):
        #ask the node if we can be neighbours
        totalsent = 0
        message = "Request|" + str(self.nodeMe.ToMessage())
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((node.ip, node.port))
            #print "__RequestToBeNeighbours, message: " + message
            while totalsent < len(message):
                sent = s.send(message[totalsent:])
                if sent == 0:
                    raise RuntimeError, "socket connection broken"
                totalsent = totalsent + sent
            try:
                SIZE = 1024
                data = s.recv(SIZE)
                #print "__RequestToBeNeighbours, Data: " + str(data)
                elements = str(data).split('|')
                if(elements[0] == "YES"):
                    if(len(elements) < self.NODE_LENGTH):
                        print "Error no guid recieved as a node"
                    message=''
                    for i in range(0,self.NODE_LENGTH):
                        message=message+str(elements[i+1])+"|"
            
                    node = Node.Node()
                    node.SetNodeFromMessage(message)
                    self.neighbourList.Add(node)
                    
            except socket.error:
                pass
                #print('Recieve failed')
        except socket.error:
            pass
            #print 'Error in send __RequestToBeNeighbours'
        s.close()
    
    def __CheckNeighbours(self):
        for node in self.neighbourList.GetAll():
            if (self.stopRun):
                return;
            val = self.__CheckNeighbour(node)
            if(not val):
                #print "Deleting neighbour: " + str(node.ip)
                self.neighbourList.Remove(node)
                
    def __CheckNeighbour(self, node):
        returnValue = False
        #create an INET, STREAMing socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        #connect to node
        try:
            #print "Check, Connecting to: " + str(node.ip) + ":" + str(node.port)
            s.connect((node.ip, node.port))
            totalsent = 0
            message = "areYouAwake"
            try:
                while totalsent < len(message):
                    sent = s.send(message[totalsent:])
                    if sent == 0:
                        raise RuntimeError, "socket connection broken"
                    totalsent = totalsent + sent
            except socket.error:
                pass
                #print('Check, Send failed')
            try:
                SIZE = 1024
                data = s.recv(SIZE)
                #print "Check, data: " + data
                elements = data.split(',')
                if(elements[0] == "YES"):
                    node.numberOfNeighbours = int(elements[1])
                    node.modified = time.time()
                    self.neighbourList.Add(node)
                    returnValue = True
                else:
                    returnValue = False
            except socket.error:
                #print('Check, Recieve failed')
                returnValue = False
            s.close()
        except socket.error:
            #print('Check, Cannot connect to: ' + str(node.ip) + ':' + str(node.port))
            returnValue = False
        return returnValue
    
    
    
    
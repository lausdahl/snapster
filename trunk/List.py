#!/usr/bin/env python

from Node import Node
from Settings import Settings
class List:
    def __init__(self):
        self.filename = "list.snapster"
        self.count = 0
        self.nodelist = []
        self.__ReadNodesFromFile()
    
    def __ReadNodesFromFile(self):
        self.nodelist = []
        for line in open(self.filename, "r").readlines():
            if(len(line)>2):
                readNode = Node()
                if (readNode.SetNodeFromMessage(line)):
                    self.nodelist.append(readNode)
                    
    def GetNodes(self):
        self.__ReadNodesFromFile()
        return self.nodelist
    
    def FindNode(self, guid):
        guid = str (guid)
        nodes = self.GetNodes()
        for node in nodes:
            if (str(node.id) == guid):
                return node
        return None
    
    def Contains(self, node):
        for n in self.GetAll():
            if(str(n.id) == str(node.id)):
                return True
        return False
    
    def ToMessage(self):
        nodesToSend = self.GetNodes()
        message = ""
        counter = 0
        for nodeToSend in nodesToSend:
            if (counter > 0):
                message += ";"
            message += nodeToSend.ToMessage()
            counter += 1
        return message
    
    def ToString(self):
        nodesToSend = self.GetNodes()
        message = ""
        counter = 0
        for nodeToSend in nodesToSend:
            message += "\n"
            message += nodeToSend.ToMessage()
            counter += 1
        return message
    
    def SetListFromMessage(self, message):
        nodesFromMessage = message.split(";")
        for s in nodesFromMessage:
            nodeFromMessage = Node()
            nodeFromMessage.SetNodeFromMessage(s)
            self.nodelist.append(nodeFromMessage)
        self.__CheckForDuplicates()
        self.SaveNodes()
    
    def SaveNodes(self):
        file = open(self.filename, "w")
        s = Settings()
        for n in self.nodelist:
            if(n.id==s.Id):
                continue
            file.write(n.ToMessage())
            file.write("\n")
        file.write("\n")
        file.close()
        
    def RemoveNodeFromList(self, node):
        newNodeList = []
        for tmpN in self.nodelist:
            if (tmpN.id != node.id):
                newNodeList.append(tmpN)
        self.nodelist = newNodeList[:]
        self.SaveNodes()
        
    def AddNode(self, node):
        
        self.nodelist.append(node)
        self.__CheckForDuplicates()
        self.SaveNodes()
    
    def Count(self):
        return len(self.nodelist)   
    
    def __CheckForDuplicates(self):
        newList = []
        self.count=0
        for n in self.nodelist:
            foundNode = False
            for newNode in newList:
                if (n.id == newNode.id and n.modified > newNode.modified):
                    foundNode = True
                    newNode.numberOfNeighbours=n.numberOfNeighbours
                    break
            if (not foundNode):
                newList.append(n)
                self.count=self.count+1
        self.nodelist = newList[:]
    
    def Clear(self):
        self.nodelist = []
        self.SaveNodes()
    
##l = List()
##print l.ToMessage()
##newMessage = "10.10.100.102|26|Hansen|9"
##l.SetListFromMessage(newMessage)
##print l.ToMessage()
    
## Testing puposes
##
##l = List()
##currentNodes = l.GetNodes()
##for tmpNode in currentNodes:
##    print tmpNode.id
##newNode = Node()
##newNode.ip = "10.10.10.10"
##newNode.port = 23
##newNode.id = "MitId"
##newNode.quality = 10
##l.AddNode(newNode)
##l.SaveNodes()
##currentNodes = l.GetNodes()
##for tmpNode in currentNodes:
##    print tmpNode.id
##l.RemoveNodeFromList(newNode)
##l.SaveNodes()
##currentNodes = l.GetNodes()
##for tmpNode in currentNodes:
##    print tmpNode.id
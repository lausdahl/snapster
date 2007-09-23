#!/usr/bin/env python

from Node import Node
from List import List
from Settings import Settings

class NeighbourList(List):
    def __init__(self):
        List.__init__(self)
        List.filename = "NeighbourList.snapster"
        self.maxNeighbours = Settings().MaxNeighbourCount
    
    def GetAll(self):
        return self.GetNodes()
    
    def Add(self, node):
        if(not self.IsFull()):
            self.AddNode(node)
    
    def Remove(self, node):
        self.RemoveNodeFromList(node)
    
    def IsFull(self):
        return self.maxNeighbours > self.count


n = NeighbourList(3)
n.Clear()

#newNode = Node()
#newNode.ip = "10.10.10.10"
#newNode.port = 23
#newNode.id = "MitddId"
#newNode.quality = 10
#
#n= NeighbourList()
#n.Add(newNode)
#p=n.IsFull()
#print p
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
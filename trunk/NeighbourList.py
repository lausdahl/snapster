from Node import Node
from List2 import List2
from Settings import Settings
class NeighbourList(List2):
    #Max=10
    def __init__(self):
        List2.filename="NeighbourList.snapster"
        List2.__init__(self)
        self.Max=Settings().MaxNeighbourCount
    def GetAll(self):
        return self.GetNodes()
    def Add(self,node):
        if(self.count<self.Max):
            self.AddNode(node)
    def Remove(self,node):
        self.RemoveNodeFromList(node)
    def IsFull(self):
        return not (self.Max-self.count)
    def Contains(self,node):
        for n in self.GetAll():
            if(n.id==node.id):
                return True
        return False
    def Clear(self):
        for n in self.GetAll():
            self.Remove(n)



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
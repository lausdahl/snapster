#!/usr/bin/env python

#Class with information about a node
import GUID
class Node:
    #def __init__(self):
    #    self.id=GUID.GUID().uuid()
    id=''
    quality=0
    port=0
    ip=''
    numberOfNeighbours=0
    fileSharePort=0
    def Show(self):
        print('ID: ' + str(self.id) +' IP: '+ str(self.ip)+' Port: '+str(self.port)+' Quality: '+str(self.quality)+ ' #Neighbour: '+ str(self.numberOfNeighbours) + ' FileSharingPort: ' + str(self.fileSharePort))
    def ToString(self):
        return ('ID: ' + str(self.id) +' IP: '+ str(self.ip)+' Port: '+str(self.port)+' Quality: '+str(self.quality)+ ' #Neighbour: '+ str(self.numberOfNeighbours)+ ' FileSharingPort: ' + str(self.fileSharePort))
    def ToMessage(self):
        return (str(self.ip)+'|'+str(self.port)+'|'+str(self.id)+'|'+str(self.quality)+'|'+str(self.numberOfNeighbours)+'|'+str(self.fileSharePort))
    def SetNodeFromMessage(self, message):
        #print(message)
        message = str(message)
        #print "Node, message: " + message
        if (message.endswith("\n")):
            message = message[:-1]
        if (message.endswith("\r")):
            message = message[:-1]
        elements = str(message).split('|')
        if (len(elements) == 0):
            return False
        try:
            count=0
            for l in elements:
                count=count+1
            self.ip = str(elements[0])
            self.port = int(elements[1])
            self.id = str(elements[2])
            self.quality = int(elements[3])
            if(count>=5):
                self.numberOfNeighbours = int(elements[4])
            else:
                self.numberOfNeighbours =0
            if(count>=6):
                self.fileSharePort = int(elements[5])
            else:
                self.fileSharePort =0
            return True
        except:
            print "Fejl i node parsing"
            #pass

#node= Node()
#node.SetNodeFromMessage("1|2|kl|4|10")
#node.Show()
#print node.ToMessage()
#node.numberOfNeighbours=30
#node.Show()
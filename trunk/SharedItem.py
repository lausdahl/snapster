#!/usr/bin/env python

import os

class SharedItem:
    def __init__(self, name=None,qualifiedname=None,size=None):
        self.name = name
        self.qualifiedname = qualifiedname
        self.size = size
        self.relevance = None
        
    def Name(self):
        return str(self.name)
    
    def Qualifiedname(self):
        return str(self.qualifiedname)
    
    #bytes
    def Size(self):
        return int(self.size)#os.path.getsize(self.Qualifiedname()))
    
    #is set when the object is returned due to a search
    def Relevance(self):
        return str(self.relevance)
    
    def ToMessage(self):
        return str(self.name) + "#" + str(self.size) + "#" + str(self.relevance)
    
    def SetFromMessage(self, message):
        elements = message.split('#')
        if (len(elements) == 3):
            self.name = elements[0]
            self.size = int(elements[1])
            self.relevance = str(elements[2])
            return True
        return False
    
    def Print(self):
        print "name: ", str(self.name)
        print "qualifiedname: ", str(self.qualifiedname)
        print "size: ", str(self.size)
        print "relevance: ", str(self.relevance)
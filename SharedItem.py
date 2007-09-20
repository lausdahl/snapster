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
    
    def Print(self):
        print "name: ", str(self.name)
        print "qualifiedname: ", str(self.qualifiedname)
        print "size: ", str(self.size)
        print "relevance: ", str(self.relevance)
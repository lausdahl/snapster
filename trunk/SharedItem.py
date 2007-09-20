#!/usr/bin/env python

class SharedItem:
    def __init__(self, name=None,qualifiedname=None,size=None):
        self.name = name
        self.qualifiedname = qualifiedname
        self.size = size
        self.relevance = None
        
    def Name(self):
        return name
    
    def Qualifiedname(self):
        return qualifiedname
    
    #bytes
    def Size(self):
        return size
    
    #is set when the object is returned due to a search
    def Relevance(self):
        return relevance
    
    def Print(self):
        print "name: ", str(self.name)
        print "qualifiedname: ", str(self.qualifiedname)
        print "size: ", str(self.size)
        print "relevance: ", str(self.relevance)
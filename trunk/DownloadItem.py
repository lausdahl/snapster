#!/usr/bin/env python

class DownloadItem:
    def __init__(self):
        self.keyword = ""
        self.filename = ""
        self.ip = ""
        self.port = 0
        self.id = 0
        self.peer = ""
        self.relevance = ""
        self.size = 0
        
    def SetFilename(self, filename):
        self.filename = filename
        
    def GetFilename(self):
        return self.filename
    
    def SetIp(self, ip):
        self.ip = ip
        
    def GetIp(self):
        return self.ip
    
    def SetId(self, id):
        self.id = int(id)
        
    def GetId(self):
        return self.id
    
    def SetSize(self, size):
        self.size = int(size)
        
    def GetSize(self):
        return self.size
        
    def SetPort(self, port):
        self.port = int(port)
        
    def GetPort(self):
        return self.port
        
    def SetKeyword(self, keyword):
        self.keyword = keyword
        
    def GetKeyword(self):
        return self.keyword
        
    def SetPeer(self, peer):
        self.peer = peer
        
    def GetPeer(self):
        return self.peer
        
    def SetRelevance(self, relevance):
        self.relevance = relevance
        
    def GetRelevance(self):
        return self.relevance
        
    def Print(self):
        print "|" + str(self.id) + "\t" + str(self.relevance) + "\t|" + self.keyword + "\t|" + self.filename + "\t|" + str(self.size) + "\t|" + self.peer
        
    def ToMessage(self):
        return str(self.id) + "|" + str(self.keyword) + "|" + str(self.filename) + "|" + str(self.size) + "|" + str(self.relevance) + "|" + str(self.ip) + "|" + str(self.port) + "|" + str(self.peer)
        
    def SetFromMessage(self, message):
        elements = message.split('|')
        if (len(elements) == 8):
            self.SetId(int(elements[0]))
            self.SetKeyword(str(elements[1]))
            self.SetFilename(str(elements[2]))
            self.SetSize(int(elements[3]))
            self.SetRelevance(str(elements[4]))
            self.SetIp(str(elements[5]))
            self.SetPort(int(elements[6]))
            self.SetPeer(str(elements[7]))
            return True
        return False
    
    
    
    
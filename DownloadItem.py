#!/usr/bin/env python

class DownloadItem:
    def __init__(self):
        self.keyword = ""
        self.filename = ""
        self.ip = ""
        self.port = 0
        self.id = 0
        self.peer = ""
        
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
        
    def Print(self):
        print "|" + str(self.id) + "\t|" + self.keyword + "\t|" + self.filename + "\t|" + self.peer
        
    def SetFromMessage(self, message):
        elements = message.split('|')
        if (len(elements) == 6):
            self.SetId(int(elements[0]))
            self.SetKeyword(str(elements[1]))
            self.SetFilename(str(elements[2]))
            self.SetIp(str(elements[3]))
            self.SetPort(int(elements[4]))
            self.SetPeer(str(elements[5]))
            return True
        return False
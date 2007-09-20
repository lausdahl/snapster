#!/usr/bin/env python
from DownloadItem import DownloadItem

class DownloadList:
    
    def __init__(self):
        self.filename = "downloadList.snapster"
        self.downloadList = []
        self.__ReadList()
        
    def __ReadList(self):
        self.downloadList = []
        for line in open(self.filename, "r").readlines():
            if(len(line) > 1):
                downloadItem = DownloadItem()
                if (downloadItem.SetFromMessage(line)):
                    self.downloadList.append(downloadItem)
    
    def __SaveList(self):
        file = open(self.filename, "w")
        for di in self.downloadList:
            file.write(str(di.GetId()) + "|" + di.GetKeyword() + "|" + di.GetFilename() + "|" + di.GetIp() + "|" + str(di.GetPort()) + "|" + di.GetPeer())
            file.write("\n")
        file.write("\n")
        file.close()
                    
    def Print(self):
        self.__ReadList()
        print "\n|Id\tRelevance\t|Keyword\t|Filename\t|Peer"
        
        for downloadItem in self.downloadList:
            downloadItem.Print()
        
        if (len(self.downloadList) == 0):
            print "No query results returned (yet)"
            
    def Add(self, downloadItem):
        self.__ReadList()
        self.downloadList.append(downloadItem)
        self.__SaveList()
        
    def Clear(self):
        file = open(self.filename, "w")
        file.close()
        
    def Remove(self, downloadItem):
        newList = []
        self.__ReadList()
        for di in self.downloadList:
            if (downloadItem.GetId() != di.GetId()):
                newList.append(di)
        self.downloadList = newList[:]
        self.__SaveList()
        
    def GetDownloadItemFromId(self, id):
        self.__ReadList()
        for di in self.downloadList:
            if (di.GetId() == id):
                return di
        return None
        
        
        
#downloadItem = DownloadItem()
#downloadItem.SetId(1)
#downloadItem.SetKeyword("Britney")
#downloadItem.SetFilename("Britney Spears - Sorry.mp3")
#downloadItem.SetIp("172.16.0.100")
#downloadItem.SetPort(8000)
#downloadItem.SetPeer("Kenneth")
#
#downloadList = DownloadList()
#downloadList.Add(downloadItem)
#downloadList.Print()
#downloadList.Remove(downloadItem)
#downloadList.Print()
#downloadList.Clear()
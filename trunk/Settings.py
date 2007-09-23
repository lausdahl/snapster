#!/usr/bin/env python

from XMLHandler import XMLHandler
from Node import Node
import os
import sys
import socket

class Settings:
    rediscovery_delay_ms = 0
    
    def __init__(self):
        self.handler = XMLHandler("Settings.xml")
        s = self.handler.ReadAppSettings()
        self.MaxNeighbourCount = int(s[0])
        self.StartServer = int(s[6])
        self.StartDiscovery = int(s[7])
        self.Port = s[4]
        self.Id = s[3]
        self.Quality = s[5]
        self.rediscovery_delay_ms = int(s[1])
        self.ip = s[2]
        self.NumberOfKWalkers = int(s[8])
        self.fileSharePort = int(s[9])
        self.Ttl = 1
        self.SharingFolderPath = os.path.join(sys.path[0], str(s[10]))
        self.DownloadFolderPath = os.path.join(sys.path[0], str(s[11]))

    def GetBootStrapNodes(self):
        return self.handler.ReadBootStrapNodes()
    
    def GetAppNode(self):
        node = Node()
        node.id = str(self.Id)
        node.ip = socket.gethostbyname(socket.gethostname())#str(self.ip)
        node.quality = int(self.Quality)
        node.numberOfNeighbours = 0
        node.port = int(self.Port)
        node.fileSharePort = int(self.fileSharePort)
        return node


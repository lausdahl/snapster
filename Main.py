#!/usr/bin/env python

import Node
import time
from Server import Server
from Client import Client
from Discovery import Discovery
from Settings import Settings
from NeighbourList import NeighbourList
from DownloadList import DownloadList
from List import List

s = Settings()
print "This node is: " + s.GetAppNode().ToString()

if(s.StartServer):
    server = Server(s.GetAppNode())
    server.start()
    time.sleep(0.5)
if(s.StartDiscovery):
    discover = Discovery(s.GetAppNode())
    discover.start()
    time.sleep(0.5)

client = Client()
client.run()
print "Client quitting"

if(s.StartDiscovery):
    print "Stopping discovery"
    discover.Stop()
if(s.StartServer):
    print "Stopping server"
    server.StopServer()

#saving state
#clear neighbour list, by moving them to global list
for n in NeighbourList().GetAll():
    List().AddNode(n)
    server.DropNode(n)
NeighbourList().Clear()

# Clear downloadlist
dL = DownloadList()
dL.Clear()
    
timeout = 2
if(s.StartDiscovery):
    while (discover.isAlive()):
        print "Discovery is still alive"
        print "Waiting " + str(timeout) + " second(s) for discovery to end..."
        time.sleep(timeout)
        
if(s.StartServer):
    while (server.isAlive()):
        print "Server is still alive"
        print "Waiting " + str(timeout) + " second(s) for server to end..."
        time.sleep(timeout)

print "Snapster has ended"

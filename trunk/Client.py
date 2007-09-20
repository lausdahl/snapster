import time
import List
from Settings import Settings
from NeighbourList import NeighbourList
from threading import Thread
from DownloadList import DownloadList
import socket

class Client(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stopRun = 0
        
    def Stop(self):
        self.stopRun = 1
        
    def run(self):
        while self.stopRun == 0:
            self.__ShowMenu()
            self.__GetInput()
    
    def __ShowMenu(self):
        print "\nYou options in Snapster:"
        print "'p' - Shows your total list of peers"
        print "'n' - Show your list of neighbours"
        print "'l' - Show list of available search results"
        print "'d ##' - will download file number ## from list (i.e.: d 12, would download item 12 from list)"
        print "'c' - Clear list of available search results"
        print "'s keywords' - Search (i.e.: s Britney Spears, would search for 'Britney Spears')"
        print "'q' - Quits this program"
        print "Remember, press 'enter' at any time to view this message again!"
    
    def __GetInput(self):
        input = raw_input("Please input your request: ")
        if(len(input) > 2 and input[0] == "s"):
            keywords = input[2:]
            self.__Search(keywords)
        elif (len(input) > 2 and input[0] == "d"):
            item = input[2:]
            self.__DownloadFile(item)
        elif (input == "l"):
            self.__ShowDownloadList()
        elif (input == "c"):
            self.__ClearDownloadList()
        elif (input == "p"):
            self.__ShowList()
        elif (input == "n"):
            self.__ShowNeighbours()
        elif (input == "q"):
            self.stopRun = 1
        else:
            print "You entered: " + input + ", which is an unknown command. Please try againg!"
    
    def __ShowNeighbours(self):
        l = NeighbourList()
        print l.ToString()
    
    def __ShowList(self):
        l = List.List()
        print l.ToString()
        
    def __ShowDownloadList(self):
        dl = DownloadList()
        dl.Print()
        
    def __ClearDownloadList(self):
        dl = DownloadList()
        dl.Clear()
        
    def __Search(self, keywords):
        print "Searching for: " + keywords
        if(len(keywords)>0):
            for n in self.__FindKWalkers():
                self.__SendQuery(str(keywords),n)
    
    def __SendQuery(self,key,reciever):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        #connect to node
        try:
            #print "Query, Connecting to: " + str(reciever.ip) + ":" + str(reciever.port)
            s.connect((reciever.ip, reciever.port))
            totalsent = 0
            message="Query|"+str(key)+"|"+str(Settings().Ttl)+"|"+str(Settings().GetAppNode().ToMessage())
            try:
                while totalsent < len(message):
                    sent = s.send(message[totalsent:])
                    if sent == 0:
                        raise RuntimeError, "socket connection broken"
                    totalsent = totalsent + sent
            except socket.error:
                print('Query, Send failed')
            s.close()
        except socket.error:
            print('ForwardQuery, Cannot connect to: ' + str(reciever.ip))
            
    def __FindKWalkers(self):
        kwCount = Settings().NumberOfKWalkers
        count = 0
        kWalker = []
        for n in NeighbourList().GetAll():
            if(count <= kwCount):
                kWalker.append(n)
                count = count + 1
        return kWalker
    
    def __DownloadFile(self, item):
        if(hostNode != None):
            dl = DownloadList()
            di = dl.GetDownloadItemFromId(item)
            if (di is None):
                return
            
            try:
                s.connect((hostNode.ip, hostNode.fileSharePort))
                
                totalsent = 0
                message = di.GetKeyword()
                
                try:
                    while totalsent < len(message):
                        sent = s.send(message[totalsent:])
                        if sent == 0:
                            raise RuntimeError, "socket connection broken"
                        totalsent = totalsent + sent
                except socket.error:
                    print('__DownloadFile, Send failed')
                
                f = open(file,"wb")
                while 1:
                    data = s.recv(1024)
                    if not data: break
                    f.write(data)
                f.close()  
            except socet.error:
                print('__DownloadFile, Recieve failed')


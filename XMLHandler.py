from xml.parsers import expat
import xml.dom.minidom #defines a standard way for accessing and manipulating XML documents
import pprint
import sys
import os
import xml.parsers.expat
from Node import Node
#import inspect
#import ErrorHandler
#import Enum



#todo: check for unique guid on creation of node
#Function writexml in minidom.py does not support elements with no data, i.e. <guid></guid>
#If the function is called (via __saveToFile) with empty elements, those will be reduced, e.g. to <guid/>, hence resulting in invalid XML. So don't do that
class XMLHandler:
    filename = ""
    dom = ""
    
    def __init__(self, filename):
        try:
            self.filename = filename
            self.dom = xml.dom.minidom.parse(self.filename)
        except IOError:
            print("No such file or directory: '" + filename +"'")
            os._exit(99)
        except expat.ExpatError:
            print(sys.exc_info()[0], ": invalid XML structure")
            os._exit(99)
        except:
            print("Exception occurred in __init__:", sys.exc_info()[0])

    def __saveToFile(self):
        try:
            file = open(self.filename, 'w')
            file.write(self.dom.toxml())
            file.close()
        except:
            print("Exception occured in __saveToFile:", sys.exc_info()[0])

    def setMaxConnections(self, value):
        try:
            for node in self.dom.getElementsByTagName('max_connections'):
                if(node.hasChildNodes()):
                    node.childNodes[0].nodeValue=value;
                else:
                    newNode = self.dom.createTextNode(value)
                    node.appendChild(newNode)
            self.__saveToFile()
        except:
            print("Exception occurred in SetMaxConnections:", sys.exc_info()[0])

    def setRediscoveryDelay(self, value):
        try:
            for node in self.dom.getElementsByTagName('rediscovery_delay_ms'):
                if(node.hasChildNodes()):
                    node.childNodes[0].nodeValue=value;
                else:
                    newNode = self.dom.createTextNode(value)
                    node.appendChild(newNode)
            self.__saveToFile()
        except:
            print("Exception occurred in SetRediscoveryDelay:", sys.exc_info()[0])

    def addBootstrapNode(self,guid,ip,port,quality):
        try:
            unique = True
            for node in self.dom.getElementsByTagName('guid'):
                if(node.hasChildNodes()):
                    if(node.childNodes[0].nodeValue == guid):
                        print("A node with guid: '" + guid + "' already exists. Add aborted")
                        unique = False
            if(unique): 
                newNode = self.dom.createElement("node")
                newGuid = self.dom.createElement("guid")
                newIp = self.dom.createElement("ip")
                newPort = self.dom.createElement("port")
                newQuality = self.dom.createElement("quality")
                
                valGuid = self.dom.createTextNode(guid)
                valIp = self.dom.createTextNode(ip)
                valPort = self.dom.createTextNode(port)
                valQuality = self.dom.createTextNode(quality)
                
                newGuid.appendChild(valGuid) #creates <guid>value</guid>
                newIp.appendChild(valIp)
                newPort.appendChild(valPort)
                newQuality.appendChild(valQuality)
                
                newNode.appendChild(newGuid) #inserts <guid>value</guid> in <node></node>
                newNode.appendChild(newIp)
                newNode.appendChild(newPort)
                newNode.appendChild(newQuality)
                
                for node in self.dom.getElementsByTagName('bootstrap'):
                   node.appendChild(newNode)
                self.__saveToFile()
        except:
            print("Exception occurred in AddBootstrapNode:", sys.exc_info()[0])
        
    def removeBootstrapNode(self,guid):
        try:
            for node in self.dom.getElementsByTagName('guid'):
                if(node.hasChildNodes()):
                    if(node.childNodes[0].nodeValue == guid):
                        node.parentNode.parentNode.removeChild(node.parentNode)
                        self.__saveToFile()
                else:
                    print("Found a node with no guid during RemoveBootstrapNode")
        except:
            print("Exception occurred in RemoveBootstrapNode:", sys.exc_info()[0])
        
    def setBootstrapNode(self,guid,ip,port,quality):
        try:
            self.RemoveBootstrapNode(guid)
            self.AddBootstrapNode(guid,ip,port,quality)
        except:
            print("Exception occurred in SetBootstrapNode:", sys.exc_info()[0])

    #returns two app settings as a list
    #exception: there is no setting

    def ReadAppSettings(self):      
        #try:
        settings = []
        settings.append(str(self.dom.getElementsByTagName('MaxNeighbourCount')[0].childNodes[0].nodeValue))
        settings.append(str(self.dom.getElementsByTagName('rediscovery_delay_ms')[0].childNodes[0].nodeValue))
        settings.append(str(self.dom.getElementsByTagName('ip')[0].childNodes[0].nodeValue))
        settings.append(str(self.dom.getElementsByTagName('id')[0].childNodes[0].nodeValue))
        settings.append(str(self.dom.getElementsByTagName('port')[0].childNodes[0].nodeValue))
        settings.append(str(self.dom.getElementsByTagName('quality')[0].childNodes[0].nodeValue))
        
        settings.append(str(self.dom.getElementsByTagName('startServer')[0].childNodes[0].nodeValue))
        settings.append(str(self.dom.getElementsByTagName('startDiscovery')[0].childNodes[0].nodeValue))
        
        settings.append(str(self.dom.getElementsByTagName('NumberOfKWalkers')[0].childNodes[0].nodeValue))
        settings.append(str(self.dom.getElementsByTagName('fileSharePort')[0].childNodes[0].nodeValue))
        settings.append(str(self.dom.getElementsByTagName('sharingFolder')[0].childNodes[0].nodeValue))
        settings.append(str(self.dom.getElementsByTagName('downloadFolder')[0].childNodes[0].nodeValue))
        
        #for conn in self.dom.getElementsByTagName('app/MaxNeighbourCount'): #run through all max_connections tags
        #    if(conn.hasChildNodes()):
        #        settings.append(int(conn.childNodes[0].nodeValue))          
        #
        #for delay in self.dom.getElementsByTagName('app/rediscovery_delay_ms'):
        #    if(delay.hasChildNodes()):
        #        settings.append(int(delay.childNodes[0].nodeValue))
        #        
        #for delay in self.dom.getElementsByTagName('app/port'):
        #    if(delay.hasChildNodes()):
        #        settings.append(int(delay.childNodes[0].nodeValue))
        #
        #for delay in self.dom.getElementsByTagName('app/id'):
        #    if(delay.hasChildNodes()):
        #        settings.append(str(delay.childNodes[0].nodeValue))
        # 
        #for delay in self.dom.getElementsByTagName('app/quality'):
        #    if(delay.hasChildNodes()):
        #        settings.append(int(delay.childNodes[0].nodeValue))
        #
        #for delay in self.dom.getElementsByTagName('app/ip'):
        #    if(delay.hasChildNodes()):
        #        settings.append(str(delay.childNodes[0].nodeValue))
                
                
        return settings
        #except:
        #    print("Exception occurred in ReadAppSettings:", sys.exc_info()[0])
        
    #returns a mapping between node-guids and the three corresponding node-values. The three values are returned as a list within the mapping  
    def ReadBootStrapNodes(self):
        mapping = []
        
        for node in self.dom.getElementsByTagName("node"):            
            nodeData = Node()
            nodeData.id= str(node.getElementsByTagName('guid')[0].childNodes[0].nodeValue)
            nodeData.ip= str(node.getElementsByTagName('ip')[0].childNodes[0].nodeValue)
            nodeData.port= int(node.getElementsByTagName('port')[0].childNodes[0].nodeValue)
            nodeData.quality= int(node.getElementsByTagName('quality')[0].childNodes[0].nodeValue)
            mapping.append(nodeData)
            #guidVal = ""
            
            #for guid in node.getElementsByTagName('guid'):
            #    if(guid.hasChildNodes()):
            #        nodeData.id= str(guid.childNodes[0].nodeValue)
            #    
            #for ip in node.getElementsByTagName('ip'):
            #    if(ip.hasChildNodes()):
            #        nodeData.ip=(str(ip.childNodes[0].nodeValue))
            #    
            #for port in node.getElementsByTagName('port'):
            #    if(port.hasChildNodes()):
            #        nodeData.port=(int(port.childNodes[0].nodeValue))
            #    
            #for quality in node.getElementsByTagName('quality'):
            #    if(quality.hasChildNodes()):
            #        nodeData.quality= (int(quality.childNodes[0].nodeValue))
                
            #mapping[guidVal] = nodeData
            
        return mapping
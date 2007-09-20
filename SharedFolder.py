#import ErrorHandler
#import inspect
from random import randrange 
import os
from os import stat
import SharedItem

#todo:  KIG PAA qsort1a:  print(relevancelist)-  DEN SORTERER IKKE TALLENE KORREKT. Er det overhovede tal? Fungerer det, hvis du giver den en list med tal
#       implement support for multiple search-parameters
class SharedFolder:
    #errhandler = ErrorHandler.ErrorHandler()
    mapping = {}
    sharedfiles = 0
    sharedfolders = 0
    
    def __init__(self,path):
        self.path = path
        
        if self.__checkpath(self.path):
            self.__walk()

    def __walk(self):
        os.path.walk(self.path,self.__collectInfo,None)
        
    #flst:names of the files in curdir
    #NOTE: the filenames are used as keys, hence identical filenames although in different folders will be skipped
    def __collectInfo(self,arg,curdir,flst):
        for name in flst:
            qualifiedname = str(curdir + "\\" + name)
            lowcasename = (str(name)).lower()
            if os.path.isfile(qualifiedname):
                if self.mapping.has_key(lowcasename):
                    pass#self.errhandler.printErrorMsg(ErrorHandler.ERRORCODE.Error,inspect.stack()[1][4],"File: '" + name +"' has one or more duplicates. Cannot be added!")
                else:
                    item = SharedItem.SharedItem(name,qualifiedname,os.path.getsize(qualifiedname))
                    self.mapping[lowcasename] = item
                    self.sharedfiles = self.sharedfiles + 1
                
        self.sharedfolders = self.sharedfolders + 1

    def __checkpath(self,path):
        if not os.path.isdir(path):
            #self.errhandler.printErrorMsg(ErrorHandler.ERRORCODE.Error,inspect.stack()[1][4],"No such directory: '" + path +"'")
            return False
        else:
            return True

    def __relevance(self,lentotal,lenfraction,digits):
        if lenfraction == 0:
            return "0"
        else:
            pctraw = str((float(lentotal) / float(lenfraction)) *100)
            pct = ""
            digits = 2 + pctraw.find(".")
           
            for char in pctraw:
                pct = pct + pct.join(char)
                if digits == 0: #we have the required number of digits
                    break
                digits = digits - 1
            return pct

    def UpdateSharedFilesList(self):
        self.mapping = {}
        self.__walk()

    def ReadFromKey(self):
        pass
    
    #return true if a match is found, otherwise return false
    #a match is defined as the case where a single char or more is identified in the name of a shared file
    #the name of a shared file is the key in the dictionary
    def Contains(self,key):
        key = key.lower()
        match = False
        if key != " " and key != "":
            if self.mapping.has_key(key):
                match = True
            else:
                for name in self.mapping:
                    if -1 != str(name).find(key):
                        match = True
                        break
        return match
        """ret = []
        key = key.lower()
        if key != " " and key != ""):
            if self.mapping.has_key(key)):
                item = self.mapping[key]
                item.relevance = self.__relevance(len(key),len(key),4)
                ret.append(item)
            else:
                for name in self.mapping:
                    if -1 != str(name).find(key)):
                        item = self.mapping[name]
                        item.relevance = self.__relevance(len(key),len(name),4)
                        ret.append(item)
        return ret"""
    
    #returns the first hit stumpled upon without regard for relevance, i.e. even if a file with higher relevance exists, we don't care
    def GetSharedFileInfo(self,key):
        key = key.lower()
        item = SharedItem.SharedItem()
        if key != " " and key != "": #we only traverse the dictionary if we have to
            if self.mapping.has_key(key):
                item = self.mapping[key]
                item.relevance = self.__relevance(len(key),len(key),4)
            else:
                for name in self.mapping:
                    if -1 != str(name).find(key):
                        item = self.mapping[name]
                        item.relevance = self.__relevance(len(key),len(name),4)
        return item
    """
    def __sortmapping(self,list):
        relevancelist = []
        ret = []
       for item in list:
            relevancelist.append(float(item.relevance))
    
        sortedrelevancelist = self.qsort(relevancelist) #sorted list of hit-percentages
        run = True
        while(run):    
            for item2 in list:
                for i in range(len(sortedrelevancelist)):
                    #print(len(ret),"  ",len(sortedrelevancelist))
                    #print("compare:", float(item2.relevance), " with ",float(item3))
                    if float(item2.relevance) == float(sortedrelevancelist[i]):
                        ret.append(item2)
                    if len(ret) == len(sortedrelevancelist):
                        run = False;
                        break
        return ret
    
    def qsort(self,list):
        if list == []:
            return []
        else:
            pivot = list.pop(randrange(len(list)))
            lesser = self.qsort([l for l in list if l.relevance < pivot])
            greater = self.qsort([l for l in list if l.relevance >= pivot])
            return lesser + [pivot] + greater
        
    #def qsort(self,list):
    #    if list == []:
    #        return []
    #    else:
    #        pivot = list.pop(randrange(len(list)))
    #        lesser = self.qsort([l for l in list if l < pivot])
    #        greater = self.qsort([l for l in list if l >= pivot])
    #        return lesser + [pivot] + greater
    """
    def SharedFilesCount(self):
        return self.sharedfiles
    
    def SharedFoldersCount(self):
        return self.sharedfolders
    
    def SetSharedFolderPath(self, path):
        if self.__checkpath(self.path):
            self.path = path
        
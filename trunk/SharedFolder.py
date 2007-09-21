#import ErrorHandler
#import inspect
from random import randrange 
import os
from os import stat
import SharedItem

#todo: implement support for multiple search-parameters
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

    #returns an sorted list of SharedItem objects, i.e. the list is sorted according to relevance (highest first)
    def GetSharedFiles(self,key):
        ret = []
        key = key.lower()
        item = SharedItem.SharedItem()
        if key != " " and key != "": #we only traverse the dictionary if we have to
            if self.mapping.has_key(key):
                item = self.mapping[key]
                item.relevance = self.__relevance(len(key),len(key),4)
                ret.append(item)
            else:
                for name in self.mapping:
                    if -1 != str(name).find(key):
                        item = self.mapping[name]
                        item.relevance = self.__relevance(len(key),len(name),4)
                        ret.append(item)
        return self.__sort(ret)
    
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
   
    def SharedFilesCount(self):
        return self.sharedfiles
    
    def SharedFoldersCount(self):
        return self.sharedfolders
    
    def SetSharedFolderPath(self, path):
        if self.__checkpath(self.path):
            self.path = path
            
    #implementation of the quicksort algorithm. It maintains 3 lists x, y and pivot (pivot should be selected randomly)
    #in pseudo code, the method does the following:
    #
    #   select a pivot value from list (one-dimensional list)
    #   for each x,y in list (where x and y traverse the same objects in list)
    #        if x.relevance < pivot.relevance then add x to less
    #        if y.relevance = pivot.relevance then add x to pivotList
    #        if y.relevance > pivot.relevance then add x to greater
    #   concatenate(quicksort(less), pivotList, quicksort(greater))
    #
    #the lists less, pivotList and greater are not directly present as variables in this implementation due to list comprehensions in Python
    #
    # concatenate(quicksort(less), pivotList, quicksort(greater)) ~ self.__sort(...) + [pivot] + self.__sort(...)
    def __sort(self,list):
        if list == []: return []
        pivot = list[0]
        return  self.__sort([x for x in list[1:] if float(x.relevance) >= float(pivot.relevance)]) + [pivot] + \
                self.__sort([y for y in list[1:] if float(y.relevance) < float(pivot.relevance)])
        
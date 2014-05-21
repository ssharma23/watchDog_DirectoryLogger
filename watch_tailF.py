from __future__ import print_function
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import datetime
import threading
import sys


gFileDict = {}
gPath = str(sys.argv[1])
gextn = str(sys.argv[2])

def initialiseFileDict():


        dirPath = gPath

        log_list = os.listdir(dirPath)
        extn = gextn
        for log in log_list:
                if log.endswith(extn):
                        logname = dirPath + "/" + log.split('.')[0]
                        gFileDict[logname] = getNewSize(logname)


def getNewSize(filePath):
        filePath = str(filePath) + gextn

        try:
                fopen = open(filePath,"r")

                fopen.seek(0,2)
                new_size = fopen.tell()
                fopen.close()
                return new_size
        except:
                return -1



def readNewData(offset,filePath,new_size):

        filePath = str(filePath) + ".log"
        fopen = open(filePath,"r")
        fopen.read(int(offset)-1)
        print (fopen.read(new_size-offset),end="")
#        print fopen.read(new_size-offset)
        fopen.close()



class MyHandler(FileSystemEventHandler):

    def on_deleted(self,event):
        if event.is_directory:
                return
        filepath,extn = os.path.splitext(event.src_path)

    def on_created(self,event):
        if event.is_directory:
                return
        filepath,extn = os.path.splitext(event.src_path)
        if extn == gextn:
                gFileDict[str(filepath)] = getNewSize(filepath)

    def on_modified(self, event):
        if event.is_directory:
                return
        filepath,extn = os.path.splitext(event.src_path)
        if extn == gextn:

                offset = gFileDict[filepath]
                gFileDict[str(filepath)] = getNewSize(filepath)
                new_size = gFileDict[str(filepath)]

                readNewDataThread = threading.Thread(target=readNewData,args=(offset,filepath,new_size))
                readNewDataThread.start()



def eventHandlerThread():
    dirPath = gPath

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=dirPath, recursive=True)
    observer.start()
    flag = True

    try:
        while flag:
            time.sleep(30000)
#           flag = False
        observer.stop()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":

        initialiseFileDict()
        eventThread = threading.Thread(target = eventHandlerThread)
        eventThread.start()
                                                                                                                                                                                           57,1          Bot

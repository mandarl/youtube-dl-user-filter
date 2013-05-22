#!/opt/usr/bin/python

#http://gdata.youtube.com/feeds/base/videos?author=CNETTV&fields=entry%28link[@rel=%27alternate%27]%28@href%29%29

#python youtube-dl-user-filter.py


import xml.etree.ElementTree as ET
import urllib
import os
import subprocess
import re
import time
import sys, traceback
import pprint


def getSettings():
    tree = ET.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.xml'))
    settings = tree.getroot()
    return settings
    
    
def getUploadedVideoIds(userName):
    videoIdDict = {}
    url = 'http://gdata.youtube.com/feeds/base/videos?author=' + userName + '&orderby=published&fields=entry%28title%2Clink[@rel=%27alternate%27]%28@href%29%29'
    feed = ET.parse(urllib.urlopen(url)).getroot()
    for entry in feed:
        videoId = entry[1].attrib['href']
        videoIdDict[videoId] = entry[0].text
        #videoIdDict['9pmPa_KxsAM'] = 'Google I/O 2013: Keynote'
    return videoIdDict
    
def checkFolder(folderPath):
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath, 0755)
        
def checkDoneFolder(basePath):
    doneFolderPath = os.path.join(basePath, '.done')
    checkFolder(doneFolderPath)
    return doneFolderPath

def cleanDirectory(directoryPath, daysToKeep):
    try:
        now = time.time()
        count = 0;
        for f in os.listdir(directoryPath):
            count = count + 1
            #print '\r\nfile found:' + f
            #print 'date:' + str(os.stat(os.path.join(directoryPath, f)).st_mtime)
            #print 'target date:' + str(now - daysToKeep * 86400)
            #print 'daysToKeep:' + str(daysToKeep) + '\r\n'
            if os.stat(os.path.join(directoryPath, f)).st_mtime < now - daysToKeep * 86400:
                if os.path.isfile(os.path.join(directoryPath, f)):
                    print 'deleting file:' + f
                    os.remove(os.path.join(directoryPath, f))
        #if count == 0:
            #os.remove(directoryPath)
    except Exception as e:
        print 'Error deleting file:' + str(e)
        #print traceback.format_exception(*sys.exc_info())

def getVideoHash(videoId):
    match = re.search('v\=([^&]+)', videoId)
    if match:
        return match.group(1)
    else:
        return 'blah'
        
def isVideoDone(basePath, videoHash):
    doneFilePath = os.path.join(basePath, '.done', videoHash)
    if os.path.isfile(doneFilePath):
        return True
    else:
        return False

def touch(fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)

def setVideoDone(basePath, videoHash):
    doneFilePath = os.path.join(basePath, '.done', videoHash)
    if not os.path.isfile(doneFilePath):
        touch(doneFilePath)

def getExecutableName():
    osname = os.name
    if osname == 'posix':
        executable = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'youtube-dl')
    elif osname == 'nt':
        executable = 'python ' + os.path.join(os.path.dirname(os.path.realpath(__file__)), 'youtube-dl')
    else:
        raise Exception('Unknown OS: this script only works on NT or POSIX')
    return executable
    

def processUser(user, basePath):
    userName = user.attrib['name']
    try:
        maxQuality = user.attrib['maxQuality']
    except KeyError:
        maxQuality = "18"
    print 'Processing user: ' + userName
    videoIdDict = getUploadedVideoIds(userName)
    for folder in user:
        try:
            daysToKeep = float(folder.attrib['daysToKeep'])
        except KeyError:
            daysToKeep = 30.0
        folderName = folder.attrib['name']
        print '\t|-- Processing folder: ' + folderName
        folderPath = os.path.join(basePath, folderName)
        folderPattern = folder.attrib['pattern']
        prog = re.compile(folderPattern)
        checkFolder(folderPath)
        for videoId,videoTitle in videoIdDict.iteritems():
            videoHash = getVideoHash(videoId)
            #print videoHash + ':' + str(isVideoDone(basePath, videoHash))
            if not isVideoDone(basePath, videoHash):
                result = prog.search(videoTitle)
                if result:
                    print '\n\t\t|-- Processing video: ' + videoTitle.encode('utf-8')
                    executable = getExecutableName()
                    argument = ' --output "' + folderPath + os.sep + '%(upload_date)s-%(stitle)s.%(ext)s" --max-quality ' + maxQuality + ' --match-title "' + folderPattern + '" "'+ videoId + '"'
                    command = executable + argument
                    ret = 1
                    ret = os.system(command)
                    if ret == 0:
                        print '*****download successfull'
                        setVideoDone(basePath, videoHash)
                    else:
                        print '*****download unsuccessfull - will try again on next iteration'
        cleanDirectory(folderPath, daysToKeep)


def main():
    settings = getSettings()
    basePath = settings.attrib['baseDirectoryPath']
    doneFolderPath = checkDoneFolder(basePath)
    for user in settings:
        processUser(user, basePath)

main()

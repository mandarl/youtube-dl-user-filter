

#http://gdata.youtube.com/feeds/base/videos?author=CNETTV&fields=entry%28link[@rel=%27alternate%27]%28@href%29%29

#python youtube-dl-user-filter.py

import xml.etree.ElementTree as ET
import urllib
import os
import subprocess
import re
import time
import sys, traceback


def getSettings():
    tree = ET.parse('settings.xml')
    settings = tree.getroot()
    return settings
    
def getTitle(videoId):
    executable = getExecutableName()
    argument = ' --get-title "' + videoId + '"'
    command = executable + argument
    proc =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    title = proc.stdout.readline()
    proc.stdout.readline()
    return title

    
def getUploadedVideoIds(userName):
    videoIdDict = {}
    url = 'http://gdata.youtube.com/feeds/base/videos?author=' + userName + '&orderby=published&fields=entry%28link[@rel=%27alternate%27]%28@href%29%29'
    feed = ET.parse(urllib.urlopen(url)).getroot()
    for entry in feed:
        for link in entry:
            videoId = link.attrib['href']
            videoIdDict[videoId] = getTitle(videoId)
    return videoIdDict
    
def checkFolder(folderPath):
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath, 0755)

def cleanDirectory(directoryPath, daysToKeep):
    try:
        now = time.time()
        for f in os.listdir(directoryPath):
            if os.stat(os.path.join(directoryPath, f)).st_mtime < now - daysToKeep * 86400:
                print 'deleting file:' + f
                if os.path.isfile(f):
                    print 'deleting file:' + f
                    #os.remove(os.path.join(directoryPath, f))
    except Exception as e:
        print 'Error deleting file!'
        print traceback.format_exception(*sys.exc_info())

def getExecutableName():
    osname = os.name
    if osname == 'posix':
        executable = '.' + os.sep + 'youtube-dl'
    elif osname == 'nt':
        executable = 'python youtube-dl'
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
        cleanDirectory(folderPath, daysToKeep)
        for videoId,videoTitle in videoIdDict.iteritems():
            result = prog.search(videoTitle)
            if result:
                print '\n\t\t|-- Processing video: ' + videoTitle
                executable = getExecutableName()
                argument = ' --output "' + folderPath + os.sep + '%(upload_date)s-%(stitle)s.%(ext)s" --max-quality ' + maxQuality + ' --match-title "' + folderPattern + '" "'+ videoId + '"'
                command = executable + argument
                ret = os.system(command)
                if ret == 0:
                    print '*****download successfull'
                else:
                    print '*****download unsuccessfull - will try again on next iteration'


def main():
    settings = getSettings()
    basePath = settings.attrib['baseDirectoryPath']
    print basePath
    for user in settings:
        processUser(user, basePath)

main()

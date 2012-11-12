

#http://gdata.youtube.com/feeds/base/videos?author=CNETTV&fields=entry%28link[@rel=%27alternate%27]%28@href%29%29

#python youtube-dl-user-filter.py

import xml.etree.ElementTree as ET
import urllib
import os
import subprocess
import re


def getSettings():
    tree = ET.parse('settings.xml')
    settings = tree.getroot()
    return settings
    
def getUploadedVideoIds(userName):
    videoIds = []
    url = 'http://gdata.youtube.com/feeds/base/videos?author=' + userName + '&orderby=published&fields=entry%28link[@rel=%27alternate%27]%28@href%29%29'
    feed = ET.parse(urllib.urlopen(url)).getroot()
    for entry in feed:
        for link in entry:
            videoIds.append(link.attrib['href'])
    return videoIds
    
def checkFolder(folderPath):
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath, 0755)

def getExecutableName():
    osname = os.name
    if osname == 'posix':
        executable = '.' + os.sep + 'youtube-dl'
    elif osname == 'nt':
        executable = 'python youtube-dl'
    else:
        raise Exception('Unknown OS: this script only works on NT or POSIX')
    return executable
    
def getTitle(videoId):
    executable = getExecutableName()
    argument = ' --get-title "' + videoId + '"'
    command = executable + argument
    proc =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    title = proc.stdout.readline()
    proc.stdout.readline()
    return title

def processUser(user, basePath):
    userName = user.attrib['name']
    try:
        maxQuality = user.attrib['maxQuality']
    except KeyError:
        maxQuality = "18"
    print maxQuality
    print 'Processing user: ' + userName
    videoIds = getUploadedVideoIds(userName)
    for folder in user:
        folderName = folder.attrib['name']
        print '\t|-- Processing folder: ' + folderName
        folderPath = os.path.join(basePath, folderName)
        folderPattern = folder.attrib['pattern']
        prog = re.compile(folderPattern)
        checkFolder(folderPath)
        for videoId in videoIds:
            title = getTitle(videoId)
            result = prog.search(title)
            if result:
                print '\t\t|-- Processing video: ' + title
                executable = getExecutableName()
                argument = ' -o "' + folderPath + os.sep + '%(upload_date)s-%(stitle)s.%(ext)s" --quiet --match-title "' + folderPattern + '" "'+ videoId + '"'
                command = executable + argument
                os.system(command)


def main():
    settings = getSettings()
    basePath = settings.attrib['baseDirectoryPath']
    print basePath
    for user in settings:
        processUser(user, basePath)

main()

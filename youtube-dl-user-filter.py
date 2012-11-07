

#http://gdata.youtube.com/feeds/base/videos?author=CNETTV&fields=entry%28link[@rel=%27alternate%27]%28@href%29%29

#python youtube-dl-user-filter.py

import xml.etree.ElementTree as ET
import urllib


def getSettings():
    tree = ET.parse('settings.xml')
    settings = tree.getroot()
    return settings
    
def getUploadedVideoIds(userName):
    videoIds = []
    url = 'http://gdata.youtube.com/feeds/base/videos?author=' + userName + '&fields=entry%28link[@rel=%27alternate%27]%28@href%29%29'
    feed = ET.parse(urllib.urlopen(url)).getroot()
    for entry in feed:
        for link in entry:
            videoIds.append(link.attrib['href'])
    return videoIds
    
def checkFolder(folderName, basePath):
    folderPath = folderName + basePath
    if(os.path.isdir(folderPath)):
        print 'here'


def processUser(user):
    userName = user.attrib['name']
    print 'Processing user:' + userName
    videoIds = getUploadedVideoIds(userName)
    for folder in user:
        folderName = folder.attrib['name']
        folderPattern = folder.attrib['pattern']
        checkFolder(folderName)


def main():
    settings = getSettings()
    basePath = settings.attrib['baseDirectoryPath']
    print baseFolder
    for user in settings:
        #processUser(user)
    
main()
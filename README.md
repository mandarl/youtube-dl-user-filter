youtube-dl-user-filter
======================

Python script to download youtube videos uploaded by specified users and filters

**TODO:**
* ~~Make sure download happens async so that parallel downloads dont choke b/w.~~
* Error handling
* Unit tests
* ~~Reduce calls to youtube, cache titles in hashmap~~
* ~~Save done videos list in .done folder~~


**Youtube Quality constants:** http://en.wikipedia.org/wiki/YouTube#Quality_and_codecs


**settings.xml example:**
`````xml
<?xml version="1.0"?>
<!-- All folders will be created relative to the baseDirectoryPath -->
<root baseDirectoryPath="./data">
    <user name="PBSNewsHour" maxQuality="18">
        <!-- Download all videos  with the title matching the regex pattern (Shields|Brooks) 
              and put them in a folder named "Shields and Brooks"-->
        <folder name="Shields and Brooks" pattern="(Shields|Brooks)" daysToKeep="30" />
    </user>
    <user name="setindia" maxQuality="18">
        <folder name="Sony\Adaalat" pattern="^Adaalat" daysToKeep="10" />
        <folder name="Sony\Bade Acche Lagte Hai" pattern="^Bade Acche Lagte Hai" daysToKeep="10" />
    </user>
    
    <user name="BloombergUTV" maxQuality="18">
        <folder name="BloombergUTV\TheOutsider" pattern="^The Outsider" daysToKeep="30" />
        <folder name="BloombergUTV\Aspire" pattern="^Aspire" daysToKeep="10" />
    </user>
    
    <user name="ndtv" maxQuality="18">
        <folder name="NDTV\Walk The Talk" pattern="^Walk The Talk" daysToKeep="10" />
        <folder name="CNBC\Storyboard" pattern="^Storyboard" daysToKeep="10" />
    </user>
    
    <user name="sanjeevkapoorkhazana" maxQuality="18">
        <folder name="Sanjeev Kapoor Khazana" pattern="^.*" daysToKeep="180" />
    </user>
    
    <user name="zeemarathi" maxQuality="18">
        <folder name="Zee Marathi\Tu Tithe Mi" pattern="^Tu Tithe Mi" daysToKeep="20" />
        <folder name="Zee Marathi\Khupte Tithe Gupte" pattern="^Khupte Tithe Gupte" daysToKeep="20" />
        <folder name="Zee Marathi\Aamhi Saare Khavayye" pattern="^Aamhi Saare Khavayye" daysToKeep="20" />
    </user>
</root>

`````


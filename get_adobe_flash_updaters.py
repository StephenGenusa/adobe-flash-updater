#!/usr/bin/env python
# Update to the latest Adobe Flash players
# Limited to Windows right now though easy to change

import os
import sys
import urllib2
import subprocess
from BeautifulSoup import BeautifulSoup

if len(sys.argv) == 2 and sys.argv[1] == '-u':
    url_opener = urllib2.urlopen('http://www.some_domain.com/flashu/g_flash.zip')
    data = url_opener.read()
    open('g_flash.zip', "wb").write(data)
    print 'Downloaded g_flash.zip'
    sys.exit()

url = 'http://www.adobe.com/products/flashplayer/distribution3.html'

conn = urllib2.urlopen(url)
html = conn.read()

soup = BeautifulSoup(html)
links = soup.findAll('a')

download_counter = 0
for tag in links:
    link = tag.get('href',None)
    if link != None and link.find('.msi') > -1 and link.find('/download') > -1:
        try:
            strfilename = link.rsplit('/', 1)[1]
            if not os.path.exists(strfilename):
                print "Attempting download of " + link
                url_opener = urllib2.urlopen(link)
                data = url_opener.read()
                open(strfilename, "wb").write(data)
                print 'Downloaded ' + link.rsplit('/', 1)[1]
            else:
                print strfilename, "already exists. skipping download."
            subprocess.call("msiexec /quiet /passive /i " + strfilename)
            download_counter += 1
            if download_counter == 2:
                print "Downloaded latest two .msi files..."
                break
        except urllib2.HTTPError, val:
            if '404' in str(val): 
                print "Couldn't download (404) " + url
        except urllib2.URLError, val:
            print "URL Error: " + url
        except Exception, e:
            print 'General error: ' + e.message
            continue
                

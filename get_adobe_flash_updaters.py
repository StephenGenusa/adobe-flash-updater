#!/usr/bin/env python
# Update to the latest Adobe Flash players
# Limited to Windows right now though easy to change

import sys, urllib2, subprocess
from BeautifulSoup import BeautifulSoup

# -u commandline param = download update to this program
if len(sys.argv) == 2 and sys.argv[1] == '-u':
    url_opener = urllib2.urlopen('http://www.somedomain_somewhere.com/upd_flash.zip')
    data = url_opener.read()
    open('upd_flash.zip', "wb").write(data)
    print 'Downloaded upd_flash.zip'
    sys.exit()

url = 'http://www.adobe.com/products/flashplayer/distribution3.html'

conn = urllib2.urlopen(url)
html = conn.read()

soup = BeautifulSoup(html)
links = soup.findAll('a')

for tag in links:
    link = tag.get('href',None)
    if link != None and link.find('.msi') > -1 and link.find('/download') > -1:
        print "Attempting download of " + link
        try:
            url_opener = urllib2.urlopen(link)
            data = url_opener.read()
            strfilename = link.rsplit('/', 1)[1]
            open(strfilename, "wb").write(data)
            print 'Downloaded ' + link.rsplit('/', 1)[1]
            subprocess.call(strfilename)
        except urllib2.HTTPError, val:
            if '404' in str(val): 
                print "Couldn't download (404) " + url
        except urllib2.URLError, val:
            print "URL Error: " + url
        except Exception, e:
            print 'General error: ' + e.message
            continue
                

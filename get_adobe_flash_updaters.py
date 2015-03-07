#!/usr/bin/env python
""" 
Downloads the latest 2 Adobe Flash players for Windows,
the Active-X and plugin Flash players, and then does a 
no-prompt install of each of them.
This can be changed to support another O/S by a simple
change to the code
"""

import os
import sys
import urllib2
import subprocess
from BeautifulSoup import BeautifulSoup

ADOBE_FLASH_URL = 'http://www.adobe.com/products/flashplayer/distribution3.html'


def check_for_updated_downloader():
    """If the -u parameter is given the program will attempt to download
       a zip file at the given URL allowing the program to self-update
    """
    if len(sys.argv) == 2 and sys.argv[1] == '-u':
        url_opener = urllib2.urlopen('http://www.some_domain.com/flashu/g_flash.zip')
        data = url_opener.read()
        open('g_flash.zip', "wb").write(data)
        print 'Downloaded latest g_flash.zip'
        sys.exit()


def main():
    # Self-update check
    check_for_updated_downloader
    
    # Get the Flash Distribution HTML
    print "Downloading the Flash Player distribution information"
    conn = urllib2.urlopen(ADOBE_FLASH_URL)
    html = conn.read()
    
    # Parse the HTML with BeautifulSoup
    print "Parsing the HTML"
    soup = BeautifulSoup(html)
    links = soup.findAll('a')
    
    download_counter = 0
    for tag in links:
        link = tag.get('href',None)
        # Look for the .msi links
        if link != None and link.find('.msi') > -1 and link.find('/download') > -1:
            try:
                player_filename = link.rsplit('/', 1)[1]
                # Download the file if the file doesn't exist already
                if not os.path.exists(player_filename):
                    print "Attempting download of " + link
                    url_opener = urllib2.urlopen(link)
                    data = url_opener.read()
                    open(player_filename, "wb").write(data)
                    print 'Downloaded ' + link.rsplit('/', 1)[1]
                else:
                    print player_filename, "already exists. skipping download."
                # Do a quiet install of the Flash player
                print "Executing", player_filename
                subprocess.call("msiexec /quiet /passive /i " + player_filename)
                # Increment the download counter. We only want the first two
                # listed: the (1) Active-X and (2) Plugin versions
                download_counter += 1
                if download_counter == 2:
                    print "Downloaded latest two .msi files..."
                    break
            except urllib2.HTTPError, val:
                if '404' in str(val): 
                    print "Couldn't download (404) " + ADOBE_FLASH_URL
            except urllib2.URLError, val:
                print "URL Error: " + ADOBE_FLASH_URL
            except Exception, e:
                print 'General error: ' + e.message
                continue
                
if __name__ == "__main__":
    main()
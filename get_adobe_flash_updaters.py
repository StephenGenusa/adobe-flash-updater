#!/usr/bin/env python

""" 
Downloads the latest 2 Adobe Flash players for Windows,
the Active-X and plugin Flash players, and then does a 
no-prompt install of each of them.

This can be changed to support another O/S by a simple
change to the code.

Build into a single EXE file with pyInstaller
\Python27\Scripts\pyinstaller.exe --onefile get_adobe_flash_updaters.py

April 30th 2015:
  Instead of using urllib2 for downloading the installation
  I am using the Python wget module so that there is a
  progress bar on the console for each download.

June 17 2015:
  Updated Adobe URLs. Now checks the installed version numbers against
  the Adobe Web site and installs if version numbers don't match the
  latest available on Adobe's web site. Skips the download and install
  if they match.
"""

# Standard Library
import os
import sys
import urllib2
import subprocess
from _winreg import *

# 3rd Party
from BeautifulSoup import BeautifulSoup
import wget

ADOBE_FLASH_URL = 'http://www.adobe.com/products/flashplayer/distribution3.html'
SELF_UPDATE_URL = 'http://www.some_domain.com/flashu/g_flash.zip'


def check_for_updated_downloader():
    """If the -u parameter is given the program will attempt to download
       a zip file at the given URL allowing the program to self-update
    """
    if len(sys.argv) == 2 and sys.argv[1] == '-u':
        wget.download(SELF_UPDATE_URL)
        print '\nDownloaded latest g_flash.zip'
        sys.exit()


def main():
    # Self-update check
    check_for_updated_downloader()

    # Get the installed versions
    try:
      aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
      aKey = OpenKey(aReg, r"SOFTWARE\Macromedia\FlashPlayerActiveX")
      activeXVersion = QueryValueEx(aKey, "Version")[0]
      CloseKey(aKey)
    except:
      activeXVersion = ""

    try:
      aKey = OpenKey(aReg, r"SOFTWARE\Macromedia\FlashPlayerPlugin")
      pluginVersion = QueryValueEx(aKey, "Version")[0]
      CloseKey(aKey)
    except:
      pluginVersion = ""
    CloseKey(aReg)  

    print "=" * 60
    print "Adobe Flash Players Installed:"
    print "ActiveX Version is =", activeXVersion 
    print "Plug-in Version is =", pluginVersion 
    print "=" * 60
   
    # Get the Flash Distribution HTML
    print "Downloading the Current Flash Player Distribution Information"
    try:
        conn = urllib2.urlopen(ADOBE_FLASH_URL)
        html = conn.read()
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html)

        currentWebVersion = ""
        for span in soup.findAll('span'):
            if span.find("span","TextH3 LayoutSmallRow"):
                currentWebVersion = span.getText().strip().split(' ')[2]
                break

        print "Current Version is =", currentWebVersion 
        print "=" * 60
        links = soup.findAll('a')
        download_counter = 0
        for tag in links:
            link = tag.get('href',None)
            # Look for the .msi links
            if link != None and link.find('.msi') > -1 and link.find('/current/licensing/win/') > -1:
                try:
                    doDownload = False 
                    player_filename = link.rsplit('/', 1)[1]
                    if player_filename.find("active_x") > -1 and activeXVersion != "" and activeXVersion != currentWebVersion:
                      doDownload = True 
                    # Download the file if the file doesn't exist already
                    if player_filename.find("plugin") > -1 and pluginVersion != "" and pluginVersion != currentWebVersion:
                      doDownload = True 
                    if doDownload and not os.path.exists(player_filename):
                        print "Attempting download of " + link
                        wget.download(link)
                        print '\nDownloaded ' + link.rsplit('/', 1)[1]
                        # Do a quiet install of the Flash player
                        print "Executing", player_filename
                        subprocess.call("msiexec /quiet /passive /i " + player_filename)
                    else:
                        print player_filename, "already exists\n   or is already installed. Skipping."
                    # Increment the download counter. We only want the first two
                    # listed: the (1) Active-X and (2) Plugin versions
                    download_counter += 1
                    if download_counter == 2:
                        print "=" * 60
                        print "Done..."
                        break
                except urllib2.HTTPError, val:
                    if '404' in str(val): 
                        print "Couldn't download (404) " + link
                except urllib2.URLError, val:
                    print "URL Error: " + link
                    print val
                except Exception, e:
                    print 'General error: ' + e.message
                    continue
    except urllib2.HTTPError, val:
        if '404' in str(val): 
            print "Couldn't download (404) " + ADOBE_FLASH_URL
    except urllib2.URLError, val:
        print "URL Error: " + ADOBE_FLASH_URL
        print val
    except Exception, e:
        print 'General error: ' + e.message

                
if __name__ == "__main__":
    main()

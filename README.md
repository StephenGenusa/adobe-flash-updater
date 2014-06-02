Adobe Flash updater for Windows
===============================

This Python script was created to help manage Adobe Flash on a Public Library's computers where the drives are Deep Freezed during the day and then thawed after Patron hours are over. It reads the Adobe distribution3.html file, grabs the two MSI files for Windows, one for Internet Explorer and the other plug-in based browsers, and executes them. This script is compiled into an EXE and loaded on each machine. There is a self-update function invoked with -u on the commandline allowing for an updated exe/zip file to be downloaded.


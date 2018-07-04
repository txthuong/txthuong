#!/usr/bin/python
import os
import sys
import usb.core
#import win32api 

import usb
import usb.util

def detect_usb(VID,PID):
    dev = usb.core.find(idVendor=VID, idProduct=PID) # VID/PID verified by company
    if dev is None:
        raise ValueError("device not found")
    else:
        print 'detected USB device' 


def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.
    log_file = open('/home/autousr/Desktop/listfile.txt','w')
    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath
            filepath = os.path.join(root, filename)
            log_file.write(filepath+'\n')
            file_paths.append(filepath)  # Add it to the list.
    log_file.close()
    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.
detect_usb(0x1005,0xB113)   
full_file_paths = get_filepaths("/media/autousr/9ABB-0409")
log_file = open('/home/autousr/Desktop/listfile.txt', 'r')
print log_file.read()
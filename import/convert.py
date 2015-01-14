#!/usr/bin/env python
 
import os
import sys
import shutil
import chardet
 
def convert_to_utf8(filename):
    # gather the encodings you think that the file may be
    # encoded inside a tuple
    encodings = ('windows-1251', 'koi8-r', 'windows-1253', 'iso-8859-7', 'macgreek')
 
    # try to open the file and exit if some IOError occurs
    try:
        f = open(filename, 'r').read()
    except Exception:
        sys.exit(1)
 
    result = chardet.detect(f)
    charset = result['encoding']
    if charset == 'utf-8':
	data = f
    else:
        data = f.decode(charset)

    # now get the absolute path of our filename and append .bak
    # to the end of it (for our backup file)
    fpath = os.path.abspath(filename)
    newfilename = fpath + '.utf8'
    tmpfilename = fpath + '.tmp'
    # and make our backup file with shutil
    #shutil.copy(filename, newfilename)
    f = open(tmpfilename, 'w')
    f.close()
 
    # and at last convert it to utf-8
    f = open(newfilename, 'w')
    try:
        f.write(data.encode('utf-8'))
    except Exception, e:
        print e
    finally:
        f.close()

file = sys.argv[1]
convert_to_utf8(file)

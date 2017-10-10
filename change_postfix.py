import os
import sys


from sys import argv

import PIL
from PIL import Image
from exceptions import IOError
img_home = os.getenv('IMG_HOME')
slash = '/'

from gamelist import create_gamelist

nameCN_list = create_gamelist()
game_list = nameCN_list

try:
    gameid = argv[1]
    game_list = nameCN_list[gameid]
    from_postfix = 'JPG'
    to_postfix = 'jpg'
except:
    from_postfix = 'JPG'
    to_postfix = 'jpg'
    print 'doing jpg progressive for all pics'
    #print "usage: python change_postfix.py gameid"
    #sys.exit(0)

for gameid in game_list.keys():
    #change name
    setup_dir = img_home + slash + str(gameid) + slash + 'setup'
    flow_dir = img_home + slash + str(gameid) + slash + 'flow'
    end_dir = img_home + slash + str(gameid) + slash + 'end'
    stuff_dir = img_home + slash + str(gameid) + slash + 'stuff'
    home_dir = img_home + slash + str(gameid)

    print setup_dir

    dir_list = list()
    dir_list.append(setup_dir)
    dir_list.append(flow_dir)
    dir_list.append(end_dir)
    dir_list.append(stuff_dir)
    dir_list.append(home_dir)

    for directory in dir_list:
        os.chdir(directory)
        filelist = os.listdir(directory)

        for filename in filelist:
            new_filename = filename.replace(from_postfix, to_postfix)
            try:
                os.rename(filename,new_filename)
            except Exception,e:
                print e
                print 'Error 32 please close the folder or any opened file'

        filelist = os.listdir(directory)
        for filename in filelist:
            try:
                img = PIL.Image.open(filename)
                destination = filename
            except:
                print filename + " is not an image"
                continue

            try:
                img.save(destination, "JPEG", quality=80, optimize=True, progressive=True)
            except IOError:
                PIL.ImageFile.MAXBLOCK = img.size[0] * img.size[1]
                print 'image may be png'
                r,g,b,a = img.split()
                img = Image.merge("RGB",(r,g,b))
                img.save(destination, "JPEG", quality=80, optimize=True, progressive=True)
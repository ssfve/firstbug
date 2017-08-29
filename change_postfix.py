import os
import sys


from sys import argv

import PIL
from PIL import Image
from exceptions import IOError
img_home = os.getenv('IMG_HOME')
slash = '/'

try:
    gameid = argv[1]
    from_postfix = argv[2]
    to_postfix = argv[3]
except:
    print "usage: python change_postfix.py gameid from_type to_type"
    print "example: python change_postfix.py JPG jpg\n"
    sys.exit(0)

#change name
setup_dir = img_home + slash + gameid + slash + 'setup'
flow_dir = img_home + slash + gameid + slash + 'flow'
end_dir = img_home + slash + gameid + slash + 'end'
stuff_dir = img_home + slash + gameid + slash + 'stuff'

print setup_dir

dir_list = list()
dir_list.append(setup_dir)
dir_list.append(flow_dir)
dir_list.append(end_dir)
dir_list.append(stuff_dir)


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
            img.save(destination, "JPEG", quality=80, optimize=True, progressive=True)
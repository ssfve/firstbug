import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
sys.path.append('/opt/mount/anaconda2/lib/python2.7/site-packages')
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import itemfreq
slash = '/'
image = 'img'
jsFolder = 'js'
indexFolder = 'index'
pageFolder = 'page'
variablesFolder = 'variables'
index_variables_filename = 'index.variables.js'

def create_colorlist():
    color_dict = dict()
    color_dict['blue']=('#283593','#E8EAF6')
    color_dict['lime']=('#827717','#F9FBE7')
    color_dict['yellow']=('#FFEB3B','#FFFDE7')
    color_dict['orange']=('#FF6600','#FFF3E0')
    color_dict['purple']=('#6A1B9A','#F3E5F5')
    color_dict['grey']=('#616161','#F5F5F5')
    color_dict['pink']=('#AD1457','#FCE4EC')
    color_dict['green']=('#2E7D32','#E8F5E9')
    color_dict['bluegrey']=('#37474F','#CFD8DC')
    color_dict['scarlet']=('#C62828','#FFEBEE')
    color_dict['lightblue']=('#1976D2','#E3F2FD')
    color_dict['deeporange']=('#BF360C','#FBE9E7')
    color_dict['brown']=('#4E342E','#EFEBE9')
    color_dict['lightbrown']=('#795548','#EFEBE9')
    color_dict['black']=('#212121','#E0E0E0')
    color_dict['cyan']=('#00BCD4','#E0F7FA')
    return color_dict
    
def calc_avg_color(img_path):
    img = cv2.imread(img_path)
    average_color = [img[:, :, i].mean() for i in range(img.shape[-1])]
    arr = np.float32(img)
    pixels = arr.reshape((-1, 3))
    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    palette = np.uint8(centroids)
    quantized = palette[labels.flatten()]
    quantized = quantized.reshape(img.shape)
    dom_color = palette[np.argmax(itemfreq(labels)[:, -1])]
    
    

    color_hex = "#{0:02x}{1:02x}{2:02x}".format(clamp(dom_color[0]), clamp(dom_color[1]), clamp(dom_color[2]))
    return color_hex
    
def clamp(x): 
    return max(0, min(x, 255))

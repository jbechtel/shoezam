#from keras.preprocessing import image
from PIL import Image
import numpy as np
import pandas as pd
import json
import os
from .TorProxy import *
from .dataIO import *

class ImageFixer(object):
    """ given a database, finds images which can't be loaded by keras and reloads them """
    def __init__(self, database_path, img_dir):
        with open(database_path) as f:
            self.db_json = json.load(f)
        self.img_dir=img_dir
        self.check_broken_images_and_rescrape(self.img_dir)

    def check_broken_images_and_rescrape(self,img_dir):
    
        total_paths = 1
        count = 1
        success = 1
        for key,value in self.db_json.items():
            for img_path,image_url in zip(value['image_paths'],value['image_urls']):
                if os.path.exists(img_path):
                    print('\nworking on image #{}'.format(count))
                    if load_image(img_path):
                        success += 1
                    else:
                        image_data = scrape(image_url)
                        fout = open(img_path, "wb")
                        print('Re-Writing Image \n{}\n{}'.format(image_url,img_path)) 
                        fout.write(image_data)
                        fout.close()
                    count += 1

                    if success % 10 == 0:
                        renew_connection()
                total_paths += 1
        print('total paths : {}'.format(total_paths))
        print('total existing images : {}'.format(count))
        print('successfully loaded images: {}'.format(success))



def load_image(img_path):
    """ Attempts to load image given a path. Returns False
        if imsage is broken """
    try:
        img = Image.open(img_path)
        print("Success")
    except IOError:
        print("Broken image at: {}".format(img_path)) 
        return False
    return True


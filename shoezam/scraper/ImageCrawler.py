import json
import os
from .TorProxy import *
from .dataIO import *
class ImageCrawler(object):
    """ Given a json built from ParseSearch this 
        will using rotating IPs from tor to download images
        from zappos
    """

    def __init__(self, data_dir, image_dir, json_filename):
        # filenams are named as oxfords_... or boots_...
        # so splitting on underscore and taking first 
        # element gives subcategory.
        subcategory = json_filename.split('_')[0]
        with open(data_dir + json_filename) as f:
            self.database = json.load(f)

        # count tracks new images added
        # start at 1 because we renew connection every
        # count % 0 == 0
        count = 1
        # tcount is the total count of keys (images)
        tcount = 0
        for key, value in self.database.items():
            # key = url
            # gets the directory name which 
            # is standardized according to url2key
            cur_dir = url2key(key,subcategory)
            # where to store images is specified by user
            new_dir = image_dir + cur_dir
            # print updates to stdout
            print('\n**** Unique Item #{}, Total Item #{} ****'.format(count,tcount))
            print('\nworking on {}'.format(new_dir))
            # make sure that the image_urls key exists and that there 
            # are actually urls to scrape from
            if ('image_urls' in value) and (value['image_urls'] is not None):
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)
                    for i,image_url in enumerate(value['image_urls']):
                        if os.path.isfile('{}/{}_{}.jpg'.format(new_dir,cur_dir,i)):
                            continue
                        else:
                            # scrape the image and save it
                            # scrape is a method of TorProxy 
                            image_data = scrape(image_url)
                            fout = open('{}/{}_{}.jpg'.format(new_dir,cur_dir,i), "wb")
                            print('Writing Image #{}'.format(i)) 
                            fout.write(image_data)
                            fout.close()
                            count += 1 
                else:
                    print('PATH EXISTS...')
            tcount +=1
            print('\n*****************************************')
            #exit()
            if count % 10 == 0:
                # reset connection with tor
                renew_connection()







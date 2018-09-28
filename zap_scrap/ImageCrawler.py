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
        subcategory = json_filename.split('_')[0]
        with open(data_dir + json_filename) as f:
            self.database = json.load(f)
        count = 1
        tcount = 0
        for key, value in self.database.items():
            # key = url
            cur_dir = url2key(key,subcategory)
            #product_url_split = key.split('/')
            #product_id = product_url_split[-3]
            #color_id = product_url_split[-1]
            #cur_dir = subcategory + '_' + 'product_' + product_id + '_color_' + color_id
            new_dir = image_dir + cur_dir
            print('\n**** Unique Item #{}, Total Item #{} ****'.format(count,tcount))
            print('\nworking on {}'.format(new_dir))
            if ('image_urls' in value) and (value['image_urls'] is not None):
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)
                    for i,image_url in enumerate(value['image_urls']):
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
                renew_connection()







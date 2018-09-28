import glob
import json
import os

def get_all_jsons(category):
    #all_json_paths = glob.glob( os.path.join('/Users/bechtel/Work/Insight/shoezam/zap_scrap/data/', '{}_*.json'.format(category)) )
    all_json_paths = glob.glob( './data/{}_*.json'.format(category) )
    print(all_json_paths)
    return all_json_paths

def url2key(url,category):
    split_url = url.split('/')
    product_id = split_url[-3]
    color_id = split_url[-1]
    new_key = category + '_' + 'product_' + product_id + '_color_' + color_id
    return new_key

def compile_database(save_dir, category,frnt=False):
    database = dict()
    all_json_paths = get_all_jsons(category)
    count = 0
    for filename in all_json_paths:
        with open(filename) as f:
            tmp_json = json.load(f)
            for url,value in tmp_json.items():
                new_key = url2key(url,category)
                if frnt:
                    img_max = 5
                else:
                    img_max = 4
                if (new_key not in database) and ('image_urls' in value) and (len(value['image_urls'])==img_max):
                    images_exist = True
                    for img_number, image_urls in enumerate(value['image_urls']):
                        if category=='oxfords':
                            image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                        elif category=='boots':
                            image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_boots/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                        elif category=='boats':
                            image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_boats/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                        elif category=='sneakers':
                            image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_sneakers/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                        elif category=='loafers':
                            image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_loafers/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                        if not os.path.exists(image_path):
                            images_exist = False
                    like_products_exist = True
                    if ('like_products' not in value):
                        like_products_exist = False
                    elif value['like_products'] is None:
                        like_products_exist = False
                    elif len(list(value['like_products']))<4:
                        like_products_exist = False

                    if images_exist and like_products_exist:

                        count += 1
                        database[new_key] = value
                        database[new_key]['url']=url
                        image_paths = []
                        for img_number,image in enumerate(database[new_key]['image_urls']):
                            if category=='oxfords':
                                image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                            elif category=='boots':
                                image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_boots/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                            elif category=='boats':
                                image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_boats/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                            elif category=='sneakers':
                                image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_sneakers/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                            elif category=='loafers':
                                image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_loafers/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'

                            image_paths.append(image_path)
                        like_product_keys = [None]*4
                        for like_product_num, like_product_url in enumerate(list(database[new_key]['like_products'])):
                            like_key = url2key(like_product_url,category)
                            like_product_keys[like_product_num] = like_key
                        database[new_key]['like_product_keys'] = like_product_keys
                        database[new_key]['image_paths']=image_paths

    print('\n*** Total number of unique entries = {} ***\n'.format(count))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open('{}/{}_db.json'.format(save_dir,category),'w') as fp:
        json.dump(database, fp, sort_keys=True, indent=4)

def frnt_compile_database(save_dir,category):
    subcategory = category.split('_')[0]
    with open('{}/{}_db.json'.format(save_dir,subcategory)) as f:
        database =json.load(f)

    all_json_paths = get_all_jsons(category)
    count = 0
    ref_database = dict()
    for filename in all_json_paths:
        with open(filename) as f:
            tmp_json = json.load(f)
        for url,value in tmp_json.items():
            new_key = url2key(url,subcategory)
            if (new_key in database) and (new_key not in ref_database) and ('image_urls' in value) and (len(value['image_urls'])==1) and ('image_urls' in database[new_key]) and (len(database[new_key]['image_urls'])==4) and ('image_paths' in database[new_key]) and (len(database[new_key]['image_paths'])==4):
                old_urls = database[new_key]['image_urls']
                new_url = value['image_urls'][0]
                img_number = 4
                if subcategory=='oxfords':
                    image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                elif subcategory=='boots':
                    image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_boots/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                elif subcategory=='boats':
                    image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_boats/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'
                elif subcategory=='sneakers':
                    image_path =  '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_sneakers/' + new_key + '/' + new_key + '_' + str(img_number) + '.jpg'

                old_paths = database[new_key]['image_paths']
                old_paths.append(image_path)
                old_urls.append(new_url)
                ref_database[new_key] = database[new_key]
                ref_database[new_key]['image_paths'] = old_paths
                ref_database[new_key]['image_urls'] = old_urls
                count+=1

    

    print('\n*** Total number of unique entries = {} ***\n'.format(count))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open('{}/{}_db.json'.format(save_dir,category),'w') as fp:
        json.dump(ref_database, fp, sort_keys=True, indent=4)


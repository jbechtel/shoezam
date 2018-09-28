from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input
from keras.models import Model
import numpy as np
import pandas as pd
from keras.utils.vis_utils import plot_model
import json
import os

from keras.applications.vgg16 import decode_predictions

from scipy.spatial.distance import cosine

#def plot_VGGnet(model):
#    plot_model(model, to_file='vgg.png')

def load_image(img_path):
    #img_path = 'elephant.jpg'
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        print("Success")
    except OSError:
        print("Broken image at: {}".format(img_path)) 
        return None
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def feature_extraction(base_model,layer_name,img_path):
    model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer_name).output)
    x = load_image(img_path)
    features = model.predict(x)
    return features

def predict_class(model,img_path):
    x = load_image(img_path)
    yhat = model.predict(x)
    # convert the probabilities to class labels
    label = decode_predictions(yhat)
    # retrieve the most likely result, e.g. highest probability
    label = label[0][0]
    # print the classification
    print('%s (%.2f%%)' % (label[1], label[2]*100))

def compile_data_table_without_features(base_model,database_path):
    layer_name = 'fc2'
    with open(database_path) as fp:
        db_json = json.load(fp)
    #df = pd.DataFrame()


    #brands = []
    #keys = []
    #msrps = [] 
    #sales = []
    #names = []
    #subcategories = []
    #views = []

    dict_list = []
    like_keys = []

    count = 1
    for key,value in db_json.items():
        for img_path,view in zip(value['image_paths'],['pair','top','left','right']):

            if os.path.exists(img_path):
                print('\nworking on image #{}'.format(count))
                print('name:\t{}'.format(value['name']))
                print('sale:\t{}'.format(value['sale']))
                print('msrp:\t{}'.format(value['msrp']))
                print('brand:\t{}'.format(value['brand']))
                print('subcategory:\t{}'.format(value['subcategory']))
                print('view:\t{}'.format(view))

                # make a dict that will be appended to list of dicts 
                tmp_dict = dict()
                tmp_dict['key'] = key
                tmp_dict['subcategory'] = value['subcategory']
                tmp_dict['brand'] = value['brand']
                tmp_dict['name'] = value['name']
                tmp_dict['view'] = view
                tmp_dict['msrp'] = value['msrp']
                tmp_dict['sale'] = value['sale']

                dict_list.append(tmp_dict)
                #keys.append(key)
                #brands.append(value['brand'])
                #msrps.append(value['msrp'])
                #sales.append(value['sale'])
                #names.append(value['name'])
                #subcategories.append(value['subcategory'])
                #views.append(view)

                # these are vectors
                like_keys.append(value['like_product_keys'])
                print('LIKE PRODUCT KEYS: \n{}'.format(value['like_product_keys']))
                count +=1
            else:
                print("ERROR : {} doesn't exist".format(img_path))
                continue

    #keys_df = pd.DataFrame(data=keys,columns='key')
    #brands_df = pd.DataFrame(data=brands,columns='brand')
    #msrps_df = pd.DataFrame(data=msrps,columns='msrp')
    #sales_df = pd.DataFrame(data=sales,columns='sale')
    #subcategories_df = pd.DataFrame(data=subcategories,columns='subcategory')
    #views_df = pd.DataFrame(data=brands,columns='view')


    dict_df = pd.DataFrame(data=dict_list)
    #like_keys_df = pd.DataFrame(data=like_keys)
    like_keys_df = pd.DataFrame(data=like_keys,columns=[ 'like_product_key_{}'.format(i) for i in range(0,4)])
    #features_df = pd.DataFrame(data=feature_vecs)  
    #big_df = pd.concat([keys_df,subcategories_df,brands_df,names_df,msrps_df,sales_df,like_keys_df,features_df])
    big_df = pd.concat([dict_df,like_keys_df],axis=1)
    big_df.to_csv('oxfords_data_frame_no_features.csv')
def compile_data_table(base_model,database_path):
    layer_name = 'fc2'
    with open(database_path) as fp:
        db_json = json.load(fp)
    #df = pd.DataFrame()


    #brands = []
    #keys = []
    #msrps = [] 
    #sales = []
    #names = []
    #subcategories = []
    #views = []

    dict_list = []
    feature_vecs = []
    like_keys = []

    count = 1
    for key,value in db_json.items():
        for img_path,view in zip(value['image_paths'],['pair','top','left','right']):

            if os.path.exists(img_path):
                print('\nworking on image #{}'.format(count))
                print('name:\t{}'.format(value['name']))
                print('sale:\t{}'.format(value['sale']))
                print('msrp:\t{}'.format(value['msrp']))
                print('brand:\t{}'.format(value['brand']))
                print('subcategory:\t{}'.format(value['subcategory']))
                print('view:\t{}'.format(view))

                # make a dict that will be appended to list of dicts 
                tmp_dict = dict()
                tmp_dict['key'] = key
                tmp_dict['subcategory'] = value['subcategory']
                tmp_dict['brand'] = value['brand']
                tmp_dict['name'] = value['name']
                tmp_dict['view'] = view
                tmp_dict['msrp'] = value['msrp']
                tmp_dict['sale'] = value['sale']

                dict_list.append(tmp_dict)
                #keys.append(key)
                #brands.append(value['brand'])
                #msrps.append(value['msrp'])
                #sales.append(value['sale'])
                #names.append(value['name'])
                #subcategories.append(value['subcategory'])
                #views.append(view)

                # these are vectors
                like_keys.append(value['like_product_keys'])
                feature_vecs.append(feature_extraction(base_model,'fc2',img_path))
                count +=1
            else:
                print("ERROR : {} doesn't exist".format(img_path))
                continue

    #keys_df = pd.DataFrame(data=keys,columns='key')
    #brands_df = pd.DataFrame(data=brands,columns='brand')
    #msrps_df = pd.DataFrame(data=msrps,columns='msrp')
    #sales_df = pd.DataFrame(data=sales,columns='sale')
    #subcategories_df = pd.DataFrame(data=subcategories,columns='subcategory')
    #views_df = pd.DataFrame(data=brands,columns='view')


    dict_df = pd.DataFrame(data=dict_list)
    like_keys_df = pd.DataFrame(data=like_keys,columns=[ 'like_product_key_{}'.format(i) for i in range(0,4)])
    features_df = pd.DataFrame(data=feature_vecs)  
    #big_df = pd.concat([keys_df,subcategories_df,brands_df,names_df,msrps_df,sales_df,like_keys_df,features_df])
    big_df = pd.concat([dict_df,like_keys_df,features_df],axis=1)
    big_df.to_csv('oxfords_data_frame.csv')


def check_broken_images(database_path):
    with open(database_path) as fp:
        db_json = json.load(fp)

    total_paths = 0
    count = 0
    success = 0
    for key,value in db_json.items():
        for img_path,view in zip(value['image_paths'],['pair','top','left','right']):
            if os.path.exists(img_path):
                print('\nworking on image #{}'.format(count))
                if load_image(img_path) is not None:
                    success += 1
                count += 1
            total_paths += 1
    print('total paths : {}'.format(total_paths))
    print('total existing images : {}'.format(count))
    print('successfully loaded images: {}'.format(success))

                

    #df = pd.DataFrame()

if __name__ == "__main__":
    
    #base_model = VGG19(weights='imagenet')
    #print(base_model.summary())


    ##plot_VGGnet(base_model)
    #last_layer_img_1 = feature_extraction('fc2','image.jpg')
    #image_path = 'image.jpg'
    #predict_class(base_model,image_path)
    #last_layer_img_2 = feature_extraction('fc2','image2.jpg')
    #print('cosine distance: {}'.format(cosine(last_layer_img_1,last_layer_img_2)))


    oxford_db = '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/databases/oxfords_db.json'
    check_broken_images(oxford_db)    

    #compile_data_table_without_features(base_model,oxford_db)


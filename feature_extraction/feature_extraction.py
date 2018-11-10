from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input
from keras.models import Model
import numpy as np
import pandas as pd
from keras.utils.vis_utils import plot_model
import json
import os
import time
import PIL
from keras import backend as K

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

def feature_extraction(base_model,layer_name,input_tensor):
    model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer_name).output)
    #x = load_image(img_path)
    features = model.predict(input_tensor)
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

def compile_data_table_without_features_with_frnt(database_path,meta_save_path):
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

    product_number = 1

    count = 1
    for key,value in db_json.items():
        for img_path,view in zip(value['image_paths'],['pair','top','left','right','front']):

            if os.path.exists(img_path):
                print('\nworking on image #{}'.format(count))
                print('name:\t{}'.format(value['name']))
                print('sale:\t{}'.format(value['sale']))
                print('msrp:\t{}'.format(value['msrp']))
                print('brand:\t{}'.format(value['brand']))
                print('url:\t{}'.format(value['url']))
                print('color:\t{}'.format(value['color']))
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
                tmp_dict['image_path'] = img_path
                tmp_dict['msrp'] = value['msrp']
                tmp_dict['sale'] = value['sale']
                tmp_dict['color'] = value['color']
                tmp_dict['url'] = value['url']

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

        product_number += 1
        #if (product_number>2*batch_size):
        #    break

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
    big_df.to_csv(meta_save_path)
def compile_data_table_without_features(database_path,meta_save_path,frnt=False):
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

    product_number = 1

    count = 1
    for key,value in db_json.items():
        if frnt:
            img_list = ['pair','top','left','right','front']
        else:
            img_list = ['pair','top','left','right']

        for img_path,view in zip(value['image_paths'],img_list):

            if os.path.exists(img_path):
                print('\nworking on image #{}'.format(count))
                print('name:\t{}'.format(value['name']))
                print('sale:\t{}'.format(value['sale']))
                print('msrp:\t{}'.format(value['msrp']))
                print('brand:\t{}'.format(value['brand']))
                print('url:\t{}'.format(value['url']))
                print('color:\t{}'.format(value['color']))
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
                tmp_dict['image_path'] = img_path
                tmp_dict['msrp'] = value['msrp']
                tmp_dict['sale'] = value['sale']
                tmp_dict['color'] = value['color']
                tmp_dict['url'] = value['url']

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

        product_number += 1
        #if (product_number>2*batch_size):
        #    break

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
    big_df.to_csv(meta_save_path)
def calc_feature_vectors_from_df(slimdf):
    count = 1
    product_number = 1
    product_images = []
    feature_vec_batch_list = []
    dict_list = []
    feature_vecs = []
    for i,row in slimdf.iterrows():
        product_images.append(load_image(row['image_path']))
        if product_number % batch_size == 0:
            t0 = time.time()
            input_tensor = np.concatenate(product_images) 
            t1 = time.time()
            total = t1-t0
            print('numpy concat time: {}'.format(total))
            t0 = time.time()
            print('model input shape : {}'.format(input_tensor.shape))
            model_output = feature_extraction(base_model,'fc2',input_tensor)
            t1 = time.time()
            total = t1-t0
            print('model execution time: {}'.format(total))
            print('model output shape : {}'.format(model_output.shape))
            feature_vec_batch_list.append(model_output)
        if product_number % batch_size == 0:
            product_images = []
        product_number += 1

    t0 = time.time()
    input_tensor = np.concatenate(product_images) 
    t1 = time.time()
    total = t1-t0
    print('numpy concat time: {}'.format(total))
    t0 = time.time()
    print('model input shape : {}'.format(input_tensor.shape))
    model_output = feature_extraction(base_model,'fc2',input_tensor)
    t1 = time.time()
    total = t1-t0
    print('model execution time: {}'.format(total))
    print('model output shape : {}'.format(model_output.shape))
    feature_vec_batch_list.append(model_output)
      
    K.clear_session()
    features = np.concatenate(feature_vec_batch_list)
    print('features.shape : {}'.format(features.shape))
    features_df = pd.DataFrame(data=features)
    #features_df.to_csv(features_save_path)
    return features_df
def compile_features_table(base_model,layer_name, database_path,batch_size,features_save_path,frnt=False):
    with open(database_path) as fp:
        db_json = json.load(fp)

    dict_list = []
    feature_vecs = []
    like_keys = []

    count = 1
    product_number = 1
    product_images = []
    #batch_size =2
    feature_vec_batch_list = []
    for key,value in db_json.items():
        if frnt:
            img_list = ['pair','top','left','right','front']
        else:
            img_list = ['pair','top','left','right']
        for img_path,view in zip(value['image_paths'],img_list):

            
            if os.path.exists(img_path):
                print('\nworking on image #{}'.format(count))
                print('name:\t{}'.format(value['name']))
                print('sale:\t{}'.format(value['sale']))
                print('msrp:\t{}'.format(value['msrp']))
                print('brand:\t{}'.format(value['brand']))
                print('subcategory:\t{}'.format(value['subcategory']))
                print('view:\t{}'.format(view))

                # these are vectors
                like_keys.append(value['like_product_keys'])
                product_images.append(load_image(img_path))
                #feature_vecs.append(feature_extraction(base_model,'fc2',img_path))
                count +=1
            else:
                print("ERROR : {} doesn't exist".format(img_path))
                continue
        if product_number % batch_size == 0:
            t0 = time.time()
            input_tensor = np.concatenate(product_images) 
            t1 = time.time()
            total = t1-t0
            print('numpy concat time: {}'.format(total))
            t0 = time.time()
            print('model input shape : {}'.format(input_tensor.shape))
            model_output = feature_extraction(base_model,'fc2',input_tensor)
            t1 = time.time()
            total = t1-t0
            print('model execution time: {}'.format(total))
            print('model output shape : {}'.format(model_output.shape))
            feature_vec_batch_list.append(model_output)
        if product_number % batch_size == 0:
            product_images = []
        product_number += 1
        #if (product_number>2*batch_size):
        #    break
    t0 = time.time()
    input_tensor = np.concatenate(product_images) 
    t1 = time.time()
    total = t1-t0
    print('numpy concat time: {}'.format(total))
    t0 = time.time()
    print('model input shape : {}'.format(input_tensor.shape))
    model_output = feature_extraction(base_model,'fc2',input_tensor)
    t1 = time.time()
    total = t1-t0
    print('model execution time: {}'.format(total))
    print('model output shape : {}'.format(model_output.shape))
    feature_vec_batch_list.append(model_output)
      
    K.clear_session()
    features = np.concatenate(feature_vec_batch_list)
    print('features.shape : {}'.format(features.shape))
    features_df = pd.DataFrame(data=features)

    features_df.to_csv(features_save_path)


def combine_meta_with_features(meta_save_path,features_save_path,full_save_path):
    meta_data_df = pd.read_csv(meta_save_path,index_col=0)
    meta_data_df.reset_index()
    features_df = pd.read_csv(features_save_path,index_col=0)
    meta_data_df.reset_index()
    #big_df = pd.concat([meta_data_df,features_df],axis=1)
    big_df = meta_data_df.join(features_df)
    big_df.to_csv(full_save_path)


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

def rand_flip_mask(black_mask,p):
    white_mask = black_mask.copy()
    for i in range(black_mask.shape[0]):
        for j in range(black_mask.shape[1]):
            if black_mask[i,j]==True:
                if np.random.uniform(low=0.0, high=1.0, size=None)<p:
                    white_mask[i,j]=False
    return white_mask


def change_white_to_color(color_tuple, data,p=0.5):
    #r1, g1, b1 = 255,255,255 # Original value
    min_c = 240
    r1,g1,b1 = min_c, min_c, min_c
    randf = np.random.uniform(low=0.0, high=1.0, size=None)

    (r2, g2, b2) = color_tuple # Value that we want to replace it with
    (rw, gw, bw) = (255,255,255) # Value that we want to replace it with
        
    
    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    #mask = (red == r1) & (green == g1) & (blue == b1)
    black_mask = (red >= r1) & (green >= g1) & (blue >= b1)
    white_mask = rand_flip_mask(black_mask,p)
    #print("black_mask.shape: {}".format(black_mask.shape))
    #print("black_mask:\n{}".format(black_mask))
    #print("black_mask:\n{}".format(black_mask))
    data[:,:,:3][black_mask] = [r2, g2, b2]
    data[:,:,:3][white_mask] = [rw, gw, bw]

    return data
    #im = Image.fromarray(data)
    #im.save('fig1_modified.png')

def prepare_augmented_images_from_df(slimdf):
    black_rows_list = []
    pepper_rows_list = []
    for index, row in slimdf.iterrows():
        print('INDEX: {}'.format(index))
        rowdict = row.to_dict()
        # dealing with 4 views: pair, top,left, right
        # for each image create a black backround
        # later expand to salt and pepper.
        
        # BLACK IMAGE
        black_dict = rowdict.copy()
        black_dict['view'] = rowdict['view'] + '_black'
        black_dict['image_path'] = rowdict['image_path'].split('.jpg')[0] + '_black.jpg'
        sim1_PATH = rowdict['image_path']
        #print('sim1_PATH: {}'.format(sim1_PATH))
        im_pil = PIL.Image.open(sim1_PATH)
        if im_pil.mode != 'RGB':
            print('im_pil.mode: {}'.format(im_pil.mode))
            im_pil = im_pil.convert('RGB')
        img_array = np.array(im_pil)
        black_img_array = change_white_to_color((0,0,0),img_array,p=1.0)
        black_im_pil = PIL.Image.fromarray(black_img_array)
        black_im_pil.save(black_dict['image_path'])
        black_rows_list.append(black_dict)
        # END BLACK

        # PEPPER IMAGE
        #im_pil = im_pil.rotate(0,expand=True)
        pepper_dict = rowdict.copy()
        pepper_dict['view'] = rowdict['view'] + '_pepper'
        pepper_dict['image_path'] = rowdict['image_path'].split('.jpg')[0] + '_pepper.jpg'
        sim1_PATH = rowdict['image_path']
        #print('sim1_PATH: {}'.format(sim1_PATH))
        im_pil = PIL.Image.open(sim1_PATH)
        if im_pil.mode != 'RGB':
            print('im_pil.mode: {}'.format(im_pil.mode))
            im_pil = im_pil.convert('RGB')
        img_array = np.array(im_pil)
        pepper_img_array = change_white_to_color((0,0,0),img_array,p=0.5)
        pepper_im_pil = PIL.Image.fromarray(pepper_img_array)
        pepper_im_pil.save(pepper_dict['image_path'])
        pepper_rows_list.append(pepper_dict)


    slim_df_black = pd.DataFrame(black_rows_list) 
    slim_df_pepper = pd.DataFrame(pepper_rows_list) 
    return slim_df_black,slim_df_pepper
                

    #df = pd.DataFrame()

if __name__ == "__main__":
    
    #layer_name = 'fc1'


    ##plot_VGGnet(base_model)
    #last_layer_img_1 = feature_extraction('fc2','image.jpg')
    #image_path = 'image.jpg'
    #predict_class(base_model,image_path)
    #last_layer_img_2 = feature_extraction('fc2','image2.jpg')
    #print('cosine distance: {}'.format(cosine(last_layer_img_1,last_layer_img_2)))
    subcategory = 'boots'
    #subcategory = 'boats_frnt'
    subcategory = 'oxfords_frnt'
    subcategory = 'boots_frnt'
    subcategory = 'loafers_frnt'
    subcategory = 'no_sneakers_augment'
    subcategory = 'boots_augment'
    subcategory = 'boats_aug_calc'
    subcategory = 'boats_pepper_calc'
    subcategory = 'oxfords_black_calc'
    subcategory = 'sneakers'
    #subcategory = 'oxfords'
    #subcategory = 'boats'
    #subcategory = 'fail'
    if subcategory=='oxfords':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        oxford_db = '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/databases/oxfords_db.json'
        #check_broken_images(oxford_db)    

        meta_save_path = '{}_data_frame_no_features.csv'.format(subcategory)
        batch_size = 40
        compile_data_table_without_features(oxford_db,meta_save_path)
        features_save_path = '{}_data_features_{}.csv'.format(subcategory,layer_name)
        compile_features_table(base_model,layer_name,oxford_db,batch_size,features_save_path)
        full_save_path = '{}_full_data_{}.csv'.format(subcategory,layer_name)
        combine_meta_with_features(meta_save_path,features_save_path,full_save_path)

    if subcategory=='boots':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        boots_db = '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/databases/boots_db.json'
        #check_broken_images(oxford_db)    

        meta_save_path = '{}_data_frame_no_features.csv'.format(subcategory)
        batch_size = 40
        compile_data_table_without_features(boots_db,meta_save_path)
        features_save_path = '{}_data_features_{}.csv'.format(subcategory,layer_name)
        compile_features_table(base_model,layer_name,boots_db,batch_size,features_save_path)
        full_save_path = '{}_full_data_{}.csv'.format(subcategory,layer_name)
        combine_meta_with_features(meta_save_path,features_save_path,full_save_path)
    if subcategory=='boats_frnt':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        boats_db = '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/databases/boats_frnt_db.json'
        #check_broken_images(oxford_db)    

        meta_save_path = '{}_data_frame_no_features.csv'.format(subcategory)
        batch_size = 40
        compile_data_table_without_features(boats_db,meta_save_path,frnt=True)
        features_save_path = '{}_data_features_{}.csv'.format(subcategory,layer_name)
        compile_features_table(base_model,layer_name,boats_db,batch_size,features_save_path,frnt=True)
        full_save_path = '{}_full_data_{}.csv'.format(subcategory,layer_name)
        combine_meta_with_features(meta_save_path,features_save_path,full_save_path)
    if subcategory=='boots_frnt':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        boats_db = '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/databases/boots_frnt_db.json'
        #check_broken_images(oxford_db)    

        meta_save_path = '{}_data_frame_no_features.csv'.format(subcategory)
        batch_size = 40
        compile_data_table_without_features(boats_db,meta_save_path,frnt=True)
        features_save_path = '{}_data_features_{}.csv'.format(subcategory,layer_name)
        compile_features_table(base_model,layer_name,boats_db,batch_size,features_save_path,frnt=True)
        full_save_path = '{}_full_data_{}.csv'.format(subcategory,layer_name)
        combine_meta_with_features(meta_save_path,features_save_path,full_save_path)
    if subcategory=='oxfords_frnt':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        boats_db = '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/databases/oxfords_frnt_db.json'
        #check_broken_images(oxford_db)    

        meta_save_path = '{}_data_frame_no_features.csv'.format(subcategory)
        batch_size = 40
        compile_data_table_without_features(boats_db,meta_save_path,frnt=True)
        features_save_path = '{}_data_features_{}.csv'.format(subcategory,layer_name)
        compile_features_table(base_model,layer_name,boats_db,batch_size,features_save_path,frnt=True)
        full_save_path = '{}_full_data_{}.csv'.format(subcategory,layer_name)
        combine_meta_with_features(meta_save_path,features_save_path,full_save_path)
    if subcategory=='loafers_frnt':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        boats_db = '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/databases/loafers_frnt_db.json'
        #check_broken_images(oxford_db)    

        meta_save_path = '{}_data_frame_no_features.csv'.format(subcategory)
        batch_size = 40
        compile_data_table_without_features(boats_db,meta_save_path,frnt=True)
        features_save_path = '{}_data_features_{}.csv'.format(subcategory,layer_name)
        compile_features_table(base_model,layer_name,boats_db,batch_size,features_save_path,frnt=True)
        full_save_path = '{}_full_data_{}.csv'.format(subcategory,layer_name)
        combine_meta_with_features(meta_save_path,features_save_path,full_save_path)
    if subcategory=='boats':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        boats_db = '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/databases/boats_db.json'
        #check_broken_images(oxford_db)    

        meta_save_path = '{}_data_frame_no_features.csv'.format(subcategory)
        batch_size = 40
        compile_data_table_without_features(boats_db,meta_save_path)
        features_save_path = '{}_data_features_{}.csv'.format(subcategory,layer_name)
        compile_features_table(base_model,layer_name,boats_db,batch_size,features_save_path)
        full_save_path = '{}_full_data_{}.csv'.format(subcategory,layer_name)
        combine_meta_with_features(meta_save_path,features_save_path,full_save_path)
    if subcategory=='sneakers':
        #base_model = VGG19(weights='imagenet')
        #print(base_model.summary())
        #layer_name = 'fc2'
        sneakers_db = '/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/databases/sneakers_db.json'
        #check_broken_images(oxford_db)    

        meta_save_path = '{}_data_frame_no_features.csv'.format(subcategory)
        batch_size = 40
        compile_data_table_without_features(sneakers_db,meta_save_path)
        #features_save_path = '{}_data_features_{}.csv'.format(subcategory,layer_name)
        #compile_features_table(base_model,layer_name,sneakers_db,batch_size,features_save_path)
        #full_save_path = '{}_full_data_{}.csv'.format(subcategory,layer_name)
        #combine_meta_with_features(meta_save_path,features_save_path,full_save_path)

    if subcategory=='boats_augment':
        #base_model = VGG19(weights='imagenet')
        #print(base_model.summary())
        #layer_name = 'fc2'
        slimdf = pd.read_csv('/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_df_boats.csv')
        slim_df_black, slim_df_pepper = prepare_augmented_images_from_df(slimdf)
        slim_df_black.to_csv('slim_{}_df_boats.csv'.format('black'))
        slim_df_pepper.to_csv('slim_{}_df_boats.csv'.format('pepper'))
    if subcategory=='oxfords_augment':
        #base_model = VGG19(weights='imagenet')
        #print(base_model.summary())
        #layer_name = 'fc2'
        slimdf = pd.read_csv('/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_df_oxfords.csv')
        slim_df_black, slim_df_pepper = prepare_augmented_images_from_df(slimdf)
        slim_df_black.to_csv('slim_{}_df_oxfords.csv'.format('black'))
        slim_df_pepper.to_csv('slim_{}_df_oxfords.csv'.format('pepper'))
    if subcategory=='boots_augment':
        #base_model = VGG19(weights='imagenet')
        #print(base_model.summary())
        #layer_name = 'fc2'
        slimdf = pd.read_csv('/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_df_boots.csv')
        slim_df_black, slim_df_pepper = prepare_augmented_images_from_df(slimdf)
        slim_df_black.to_csv('slim_{}_df_boots.csv'.format('black'))
        slim_df_pepper.to_csv('slim_{}_df_boots.csv'.format('pepper'))

    if subcategory=='boats_black_calc':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        batch_size = 200
        df_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_black_df_boats.csv'
        slimdf = pd.read_csv(df_path,index_col=0)
        slim_features = calc_feature_vectors_from_df(slimdf)
        slim_features_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_black_features_boats.csv'
        slim_features.to_csv(slim_features_path)

        #slim_df_black.to_csv('slim_{}_df_boats.csv'.format('black'))
        #slim_df_pepper.to_csv('slim_{}_df_boats.csv'.format('pepper'))

    if subcategory=='boats_pepper_calc':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        batch_size = 200
        df_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_pepper_df_boats.csv'
        slimdf = pd.read_csv(df_path,index_col=0)
        slim_features = calc_feature_vectors_from_df(slimdf)
        slim_features_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_pepper_features_boats.csv'
        slim_features.to_csv(slim_features_path)
    if subcategory=='boots_black_calc':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        batch_size = 200
        df_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_black_df_boots.csv'
        slimdf = pd.read_csv(df_path,index_col=0)
        slim_features = calc_feature_vectors_from_df(slimdf)
        slim_features_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_black_features_boots.csv'
        slim_features.to_csv(slim_features_path)
    if subcategory=='boots_pepper_calc':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        batch_size = 200
        df_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_pepper_df_boots.csv'
        slimdf = pd.read_csv(df_path,index_col=0)
        slim_features = calc_feature_vectors_from_df(slimdf)
        slim_features_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_pepper_features_boots.csv'
        slim_features.to_csv(slim_features_path)
    if subcategory=='oxfords_black_calc':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        batch_size = 200
        df_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_black_df_oxfords.csv'
        slimdf = pd.read_csv(df_path,index_col=0)
        slim_features = calc_feature_vectors_from_df(slimdf)
        slim_features_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_black_features_oxfords.csv'
        slim_features.to_csv(slim_features_path)
    if subcategory=='oxfords_pepper_calc':
        base_model = VGG19(weights='imagenet')
        print(base_model.summary())
        layer_name = 'fc2'
        batch_size = 200
        df_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_pepper_df_oxfords.csv'
        slimdf = pd.read_csv(df_path,index_col=0)
        slim_features = calc_feature_vectors_from_df(slimdf)
        slim_features_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/slim_pepper_features_oxfords.csv'
        slim_features.to_csv(slim_features_path)



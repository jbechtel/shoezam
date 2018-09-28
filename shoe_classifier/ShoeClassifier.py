from __future__ import absolute_import
from keras.applications.vgg19 import VGG19
import tensorflow as tf
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input
from keras.models import Model
import numpy as np
import pandas as pd
from keras.utils.vis_utils import plot_model
import json
import os
import time
from keras import backend as K
import pickle
from PIL import Image as pil_image
from scipy.spatial.distance import euclidean,cosine,cdist,squareform

_PIL_INTERPOLATION_METHODS = {
      'nearest': pil_image.NEAREST,
      'bilinear': pil_image.BILINEAR,
      'bicubic': pil_image.BICUBIC,
}

class ShoeClassifier(object):
    def __init__(self,classifier='euclidean',subcategory='no_sneakers',layer_name='fc2',top_n=10):

        self.top_n = top_n
        self.subcategory = subcategory 
        self.classifier = classifier
        #if layer_model is None:
        #    print("ERROR no keras model?")
        #else:
        #    self.layer_model = layer_model
        self.layer_name = layer_name
        self.base_model = VGG19(weights='imagenet')
        self.layer_model = Model(inputs=self.base_model.input, outputs=self.base_model.get_layer(self.layer_name).output)
        self.base_graph = tf.get_default_graph()
        #K.clear_session()
        #self.layer_model = Model(inputs=self.base_model.input, outputs=self.base_model.get_layer(self.layer_name).output)
        #print(self.base_model.summary())
        self.layer_name = layer_name
        if self.subcategory not in ['oxfords','boots','boats','sneakers','no_sneakers','frnt_no_sneakers']:
            print("In ShoeClassifier().__init__\n ERROR exiting, need to choose subcategory oxfords, boots, boats, or sneakers")
            K.clear_session()
            exit()
        if self.subcategory=='oxfords':
            odf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/oxfords_data_frame_no_features.csv'
            #oxfords_db = 'oxfords_data_frame_no_features.csv'
            # new 
            if self.classifier in ['euclidean','cosine']:
                oxf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/oxfords_data_features_fc2.csv'
                #G_eu_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/oxfords_fc1_G_eu.csv'
                #G_cos_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/oxfords_fc1_G_cos.csv'
                #self.G_eu = np.genfromtxt(G_eu_path)
                #self.G_cos = np.genfromtxt(G_cos_path)
        elif self.subcategory=='boats':
            odf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/boats_data_frame_no_features.csv'
            #oxfords_db = 'oxfords_data_frame_no_features.csv'
            # new 
            if self.classifier in ['euclidean','cosine']:
                oxf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/boats_data_features_fc2.csv'
        elif self.subcategory=='boots':
            odf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/boots_data_frame_no_features.csv'
            #oxfords_db = 'oxfords_data_frame_no_features.csv'
            # new 
            if self.classifier in ['euclidean','cosine']:
                oxf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/boots_data_features_fc2.csv'
        elif self.subcategory=='sneakers':
            odf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/sneakers_data_frame_no_features.csv'
            #oxfords_db = 'oxfords_data_frame_no_features.csv'
            # new 
            if self.classifier in ['euclidean','cosine']:
                oxf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/sneakers_data_features_fc2.csv'
        elif self.subcategory=='no_sneakers':
            odf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/no_features_data_oxfords_boats_boots.csv'
            #oxfords_db = 'oxfords_data_frame_no_features.csv'
            # new 
            if self.classifier in ['euclidean','cosine']:
                oxf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/features_fc2_data_oxfords_boats_boots.csv'
        elif self.subcategory=='frnt_no_sneakers':
            odf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/frnt_no_features_data_oxfords_boats_boots.csv'
            #oxfords_db = 'oxfords_data_frame_no_features.csv'
            # new 
            if self.classifier in ['euclidean','cosine']:
                oxf_path = '/Users/bechtel/Work/Insight/shoezam/feature_extraction/frnt_features_fc2_data_oxfords_boats_boots.csv'

        self.oxf = pd.read_csv(oxf_path,index_col=0).values
        self.odf = pd.read_csv(odf_path,index_col=0)
        self.odf.msrp = self.odf.msrp.replace('[\$,]', '', regex=True).astype(float)
        self.odf.sale = self.odf.sale.replace('[\$,]', '', regex=True).astype(float)

        if self.classifier=='auto':
            class_path = '/Users/bechtel/Work/Insight/shoezam/webapp/test_model.pkl'
            self.classifier_model = pickle.load(open(class_path, 'rb'))

        self.input_feature_vec = None
    def find_top_matches_by_path(self,img_path,user_category=None):
        self.extract_features_by_path(img_path)
        return self.find_top_matches(user_category)

    def find_top_matches_by_PIL_image(self,pillow_image,user_category=None):
        self.extract_features_by_PIL_image(pillow_image)
        return self.find_top_matches(user_category)

    def find_top_matches(self,user_category=None):
        np.set_printoptions(precision=4,suppress=True)

        if self.classifier=='auto':
            diff_vecs = abs(self.input_feature_vec - self.oxf)
            print('diff_vecs.shape : {}'.format(diff_vecs.shape))
            match_probs = self.classifier_model.predict_proba(diff_vecs)[:,1]
            print('match_probs.shape : {}'.format(match_probs.shape))
            best_args = np.argsort(match_probs)[::-1][:self.top_n]
            best_match = best_args[0]
            similar_matches = best_args[1:]
            best_match_row = self.odf.iloc[best_match,:]
            print('best_match_row : {}'.format(best_match_row))
            top_keys = []
            top_indices = []
            for i, image_index in enumerate(similar_matches):
                key = self.odf['key'].iloc[image_index]
                if key not in top_keys:
                    top_keys.append(key)
                    top_indices.append(image_index)

            print('top_indices: {}'.format(top_indices))
            print('top_keys: {}'.format(top_keys))
            prices = self.odf['msrp'].iloc[top_indices].values
            print('prices: {}'.format(prices))
            indices_in_increasing_price = np.argsort(prices)
            lowest_price_image_index = top_indices[indices_in_increasing_price[0]]
            highest_price_image_index = top_indices[indices_in_increasing_price[-1]]

            print('lowest_price_image_row :\n{}'.format(self.odf.iloc[lowest_price_image_index,:]))
            print('highest_price_image_row :\n{}'.format(self.odf.iloc[highest_price_image_index,:]))
            return best_match_row,self.odf.iloc[lowest_price_image_index,:],self.odf.iloc[highest_price_image_index,:]

        if self.classifier in ['euclidean','cosine']:
            # first compute distance between self.input_feature_vec and 
            # all other vecs
            print('self.input_feature_vec.shape: {}'.format(self.input_feature_vec.shape))

            if user_category in ['Boots','Oxfords','Boat Shoes']:
                # define rows that belong to user category 
                user_cat_idx = self.odf.index[self.odf['subcategory']==user_category].tolist()
                # get numpy feature vec by subcategory 
                oxf_by_cat = self.oxf[user_cat_idx,:]
                # get pandas by subcategory 
                odf_by_cat = self.odf.iloc[user_cat_idx,:]
            else:
                # get numpy feature vec by subcategory 
                oxf_by_cat = self.oxf
                # get pandas by subcategory 
                odf_by_cat = self.odf
            print("oxf_by_cat.shape : {} ".format(oxf_by_cat.shape))
            print("odf_by_cat.shape : {} ".format(odf_by_cat.shape))

            print('self.oxf.shape: {}'.format(self.oxf.shape))
            #distances = cdist(self.input_feature_vec,self.oxf, self.classifier)
            distances = cdist(self.input_feature_vec,oxf_by_cat, self.classifier)
            print('distances.shape : {}'.format(distances.shape))
            best_args = np.argsort(distances[0,:])[:self.top_n]
            print('distances[best_args]: \n{}'.format(distances[0,best_args]))
            print('best_args: {}'.format(best_args)) 
            best_match = best_args[0]
            similar_matches = best_args[1:]
            best_match_row = odf_by_cat.iloc[best_match,:]
            #best_match_row = self.odf.iloc[best_match,:]
            print('best_match_row : {}'.format(best_match_row))
            top_keys = []
            top_indices = []
            for i, image_index in enumerate(similar_matches):
                #key = self.odf['key'].iloc[image_index]
                key = odf_by_cat['key'].iloc[image_index]
                if key not in top_keys:
                    top_keys.append(key)
                    top_indices.append(image_index)

            print('top_indices: {}'.format(top_indices))
            print('top_keys: {}'.format(top_keys))
            #prices = self.odf['msrp'].iloc[top_indices].values
            prices = odf_by_cat['msrp'].iloc[top_indices].values
            print('prices: {}'.format(prices))
            indices_in_increasing_price = np.argsort(prices)
            lowest_price_image_index = top_indices[indices_in_increasing_price[0]]
            highest_price_image_index = top_indices[indices_in_increasing_price[-1]]

            #print('lowest_price_image_row :\n{}'.format(self.odf.iloc[lowest_price_image_index,:]))
            #print('highest_price_image_row :\n{}'.format(self.odf.iloc[highest_price_image_index,:]))
            print('lowest_price_image_row :\n{}'.format(odf_by_cat.iloc[lowest_price_image_index,:]))
            print('highest_price_image_row :\n{}'.format(odf_by_cat.iloc[highest_price_image_index,:]))
            if best_match_row is not None:
                print("best_match_row is not None")
            #if self.odf.iloc[lowest_price_image_index,:] is not None:
            if odf_by_cat.iloc[lowest_price_image_index,:] is not None:
                print("self.odf.iloc[lowest_price_image_index,:] is not None")
            #if self.odf.iloc[highest_price_image_index,:] is not None:
            if odf_by_cat.iloc[highest_price_image_index,:] is not None:
                print("self.odf.iloc[highest_price_image_index,:] is not None")
            #return best_match_row,self.odf.iloc[lowest_price_image_index,:],self.odf.iloc[highest_price_image_index,:]
            return best_match_row,odf_by_cat.iloc[lowest_price_image_index,:],odf_by_cat.iloc[highest_price_image_index,:]



    def extract_features_by_path(self,img_path):
        #K.clear_session()
        with self.base_graph.as_default():
            self.input_feature_vec = self.layer_model.predict(load_image(img_path)) 
    def extract_features_by_PIL_image(self,pillow_image):
        #K.clear_session()
        with self.base_graph.as_default():
            self.input_feature_vec = self.layer_model.predict(load_PIL_image(pillow_image)) 

     
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
def load_PIL_image(img,target_size=(224,224),interpolation='nearest'):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    if target_size is not None:
        width_height_tuple = (target_size[1], target_size[0])
        if img.size != width_height_tuple:
            #if interpolation not in _PIL_INTERPOLATION_METHODS:
            #  raise ValueError('Invalid interpolation method {} specified. Supported '
            #                   'methods are {}'.format(interpolation, ', '.join(
            #                       _PIL_INTERPOLATION_METHODS.keys())))
            resample = _PIL_INTERPOLATION_METHODS[interpolation]
            img = img.resize(width_height_tuple, resample)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def feature_extraction(layer_model,input_tensor):
    #x = load_image(img_path)
    features = layer_model.predict(input_tensor)
    return features

def print_shoe_by_index(image_index,dataframe):
    PATH = dataframe['image_path'].iloc[image_index]
    display(Image(filename = PATH, width=100, height=100))
    

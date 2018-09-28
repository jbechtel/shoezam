from __future__ import absolute_import
from bs4 import BeautifulSoup
import requests
import os
from .Misc import get_page
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from random import randint
import socks
import socket
import stem.process

from selenium.webdriver.firefox.options import Options
class ParseProduct(object):
    """ parses html product info scraped from Zappos 

    Args:
        html: html from product URL
        url: product URL
    Attributes:
        asdf    
            
    """

    def __init__(self, url,price = None):
        #product_page = get_page(url)
        #self.soup = BeautifulSoup(product_page, 'html.parser') 


        #def scrape_with_tor():
        #SOCKS_PORT=9050# You can change the port number
        #tor_process = stem.process.launch_tor_with_config(
        #    config = {
        #        'SocksPort': str(SOCKS_PORT),
        #    },
        #)
        #socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
        #                      addr="127.0.0.1",
        #                      port=SOCKS_PORT)
        #socket.socket = socks.socksocket



        # ...
        #with request.urlopen(url_request) as response:
        #        try:
        #            page = response.read()
        #        except (http.client.IncompleteRead) as e:
        #            page = e.partial
        # ...
        #tor_process.kill()
        # END scrape_with_tor
        
        # FIREFOX WITH TOR
        #profile = webdriver.FirefoxProfile()
        #profile.set_preference("network.proxy.type", 1)
        #profile.set_preference("network.proxy.socks", '127.0.0.1')
        #profile.set_preference("network.proxy.socks_port", 9150)
        #profile.set_preference("network.proxy.socks_remote_dns", False)
        #profile.update_preferences()
        
        #options = Options()
        #options.add_argument('headless')
        #driver = webdriver.Firefox(firefox_profile=profile,firefox_options=options)

        # parseSearch
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(firefox_options=options)
        #

        # The following works however Zappos blocks tor????
        #profile=webdriver.FirefoxProfile()
        #profile.set_preference('network.proxy.type', 1)
        #profile.set_preference('network.proxy.socks', '127.0.0.1')
        #profile.set_preference('network.proxy.socks_port', 9050)
        #driver=webdriver.Firefox(profile)
        # END FIREFOX WITH TOR
        # OP

        # CHROME with tor? 
        #options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        #driver = webdriver.Chrome(chrome_options=options)
        # END CHROME


        driver.get(url)
        self.like_products_exist = True
        try:
            WebDriverWait(driver, randint(1,3)).until(EC.presence_of_element_located((By.ID, 'alsoLike')))
        except TimeoutException:
            print('Page timed out after 3 secs.')
            self.like_products_exist = False
        self.soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        self.bad_link = False
        if self.soup.find('body',class_="activeMain") is None:
            self.bad_link = True
            

        #tor_process.kill()
        #print('soup: {}'.format(soup.find_all('a', {'data-type': 'You May Also Like'})))


        # product details will be populated as 
        #[ category, subcategory, brand, name, color ]
        #self.product_details = [self.category,self.subcategory,self.brand,self.name,self.color]
        self.product_details = None
        self.category = None
        self.subcategory = None
        self.brand = None
        self.name = None
        self.color = None
        self.price = price

        # like_products urls will be 4 recommended product urls
        #[ url0, url1, ...]
        self.like_products = None

        # image_urls will be 5 urls to 5 jpgs
        #[ url0, url1, ...]
        self.image_urls = None
        if self.bad_link == False:
            self.get_product_details()
            self.get_image_urls()
            # LIKE PRODUCTS MAY NOT EXIST!
            if self.like_products_exist:
                self.get_like_products()
    def get_like_products(self):
        if self.like_products is not None:
            return self.like_products
        elif self.like_products_exist:
            #alsoLike = self.soup.find('body',class_="activeMain").find('div',attrs={'id':'alsoLike'}).find_all('a',attrs={'data-type':'You May Also Like'})
            #alsoLike = self.soup.find('div',attrs={'id':'root'}).find_all('a',attrs={'data-type':'You May Also Like'})

            alsoLike = self.soup.find('div',attrs={'id':'alsoLike'}).find_all('a', {'data-type': 'You May Also Like'})
            #alsoLike = self.soup.find('div',attrs={'id':'root'}).find('div',attrs={'id':'productRecap'}).find_all('div',attrs={'id':'itemInformation'})
            #print('alsoLike: {}'.format(alsoLike))
            self.like_products = []
            for i,item in enumerate(alsoLike):
                url_end = item.attrs['href']
                clipped_end = url_end.split('?',1)[0]
                url = "https://www.zappos.com" + clipped_end
                #print(url) 
                all_text = [ t.text for t in item.find_all('span')] 
                #print(all_text)
                sale = None 
                #print('len all_text: {}'.format(len(all_text)))
                if len(all_text)==7:
                    # msrp with dollar sign str
                    msrp = all_text[-1]
                    # sale with dollar sign str
                    sale = all_text[-3]
                elif len(all_text)==5:
                    msrp = all_text[-1]
                like_product = [url,msrp,sale]
                self.like_products.append(like_product)
            return self.like_products

    def print_like_products(self):
        print("in print_product_details")
        if (self.like_products is None) and (self.like_products_exist):
            self.get_like_products()
        if self.like_products is not None:
            print("======== Like Product URLs  ========\n")
            for i,prod in enumerate(self.like_products):
                print("\n*** Product #{} ***".format(i))
                for detail,name in zip(prod,['url:   ','msrp:  ','sale:  ']):
                    print("{}\t{}".format(name,detail))
                print("*******************".format(i))
            print("\n====================================")
        else:
            print("\n NO Like Products exist...\n")
            
    def get_image_urls(self):
        print("in get_image_urls")
        if self.image_urls is not None:
            print("self.iimage_urls is not None")
            return self.image_urls
        else:
            print("Is else")
            thumbs = self.soup.find('body',class_="activeMain").find('div',attrs={'id':'thumbnailsList'})
            small_urls = []

            pair = thumbs.find('img',attrs={'alt':'PAIR'})
            if pair is not None:
                small_pair_url = pair.attrs['src']
                small_urls.append(small_pair_url)

            top  = thumbs.find('img',attrs={'alt':'TOPP'})
            if top is not None:
                small_top_url = top.attrs['src']
                small_urls.append(small_top_url)

            left  = thumbs.find('img',attrs={'alt':'LEFT'})
            if left is not None:
                small_left_url = left.attrs['src']
                small_urls.append(small_left_url)

            right  = thumbs.find('img',attrs={'alt':'RGHT'})
            if right is not None:
                small_right_url = right.attrs['src']
                small_urls.append(small_right_url)

            pair = thumbs.find('img',attrs={'alt':'FRNT'})
            print('pair = {}'.format(pair))
            if pair is not None:
                print('pair is not None')
                small_pair_url = pair.attrs['src']
                print('small_pair_url: {}'.format(small_pair_url))
                small_urls.append(small_pair_url)
            #small_urls = [ small_pair_url, small_top_url, small_left_url, small_right_url ]
            #print('small_urls: {}'.format(small_urls))
            big_urls = []
            for url in small_urls:
                big_url = url.replace('_SR106,78_','_SX480_')
                big_urls.append(big_url)
            self.image_urls = big_urls
            return self.image_urls

    def get_product_details(self):
        #print("in get_product_details")
        if self.product_details is not None:
            return self.product_details
        else:
            header_data = self.soup.find('body',class_="activeMain").find('div',attrs={'id':'breadcrumbs'}).find_all('a')#('div',class_='SRGgm')
            for i,head in enumerate(header_data):
                #print('text #{}'.format(i) + head.text)
                if i==1:
                    #print('appending: {}'.format(head.text))
                    self.category = head.text
                elif i==2:
                    #print('appending: {}'.format(head.text))
                    self.subcategory = head.text
                elif i==3:
                    #print('appending: {}'.format(head.text))
                    self.brand = head.text

            #brand_data = self.soup.find('body',class_="activeMain").find('span',attrs={'itemprop':'brand'}).find_all('a')#('div',class_='SRGgm')
            #print(brand_data)
            #brand = brand_data.text
            #name_data = self.soup.find('body',class_="activeMain").find('meta',attrs={'itemprop':'name'}).find_all('a')
            #name_data = self.soup.find('body',class_="activeMain").find_all('meta',attrs={'itemprop':'name'})
            #print(name_data)
            #self.name = name_data.attrs['content']
            name_data = self.soup.find('head').find('title').text.split()
            #print(name_data.text.split())
            #print(name_data)
            name = name_data[len(self.brand.split()):-2]
            self.name = " ".join(name) 
            #print(self.name)
            color_data = self.soup.find('body',class_="activeMain").find('meta',attrs={'itemprop':'color'})
            self.color = color_data.attrs['content']
            #print('self.color: {}'.format(self.color))

            #price_data = self.soup.find('body',class_="activeMain").find('div',attrs={'id':'stage'})
            #print(price_data)
            #price_text = self.text
            #print(price_text)
            self.product_details = [self.category,self.subcategory,self.brand,self.name,self.color]
            return self.product_details

    def print_product_details(self):
        print("in print_product_details")
        if self.product_details is None:
            self.get_product_details()
        if self.product_details is not None:
            print("======== Product Details ========\n")
            for detail,name in zip(self.product_details,['category:   ','subcategory:','brand:      ','name:       ','color:      ']):
                print("{}\t{}".format(name,detail))
            print("\n=================================")

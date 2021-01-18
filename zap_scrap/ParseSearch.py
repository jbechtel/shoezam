from __future__ import absolute_import
from bs4 import BeautifulSoup
import requests
import os
import gevent
from .Misc import get_page
from .ParseProduct import ParseProduct
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json


class ParseSearch(object):
    """ parses html search page info scraped from Zappos 

    Args:
        html: html from product URL
        url: product URL
            
    """

    def __init__(self, url,page=None,subcategory=None):
        if page is not None:
            self.page = page
        if subcategory is not None:
            self.subcategory = subcategory
        product_page = get_page(url)
        self.soup = BeautifulSoup(product_page, 'html.parser') 
        # print(self.soup)

        #driver = webdriver.Chrome()
        #driver.get(url)
        #try:
        #    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'alsoLike')))
        #except TimeoutException:
        #    print('Page timed out after 10 secs.')
        #self.soup = BeautifulSoup(driver.page_source, 'html.parser')
        #driver.quit()


        # product_urls list of urls and price for each product on the page
        #  
        self.product_list = None
        self.get_product_list()
    def get_product_list(self):
        if self.product_list is not None:
            return self.product_list
        else:
            self.product_list = []
            outer = self.soup.find("div",attrs={"class":"searchPage"})
            for i,product in enumerate(outer.find_all("article")):
                print(product.prettify())
                # name_soup = product.find('p',attrs={'itemprop':'name'}) 
                # name_soup = product.find('dl',attrs={'itemprop':'name'}) 
                name_soup = product.find('dd', attrs={'itemprop': 'name'}) 
                print(f'\n\ndd: {name_soup.prettify()}')
                name = name_soup.text
                print("NAME: {}".format(name))
                print('\n\n')
                #print('\n product #{}'.format(i))
                #all_text = [t.text for t in product.find_all('p')
                color_soup = product.find('dd', attrs={'itemprop': 'color'}) 
                print(f'\n\ndd: {color_soup.prettify()}')
                color = color_soup.text
                print("COLOR: {}".format(color))
                print('\n\n')
                brand_soup = product.find('dd', attrs={'itemprop': 'brand'}) 
                print(f'\n\ndd: {brand_soup.prettify()}')
                brand = brand_soup.text
                print("BRAND: {}".format(brand))
                print('\n\n')

                price_soup = product.find('dd', attrs={'itemprop': 'offers'}) 
                print(f'\n\ndd: {price_soup.prettify()}')
                price_info = price_soup.text.split('MSRP: ')
                print("PRICE: {}".format(price_info))
                print('\n\n')

                msrp = None
                sale = None
                # pi = [t.text for t in product.find_all('dd')]
                
                product_info = {'brand': brand, 'name': name, 'color': color}
                # price_info = pi[3].split('MSRP: ')
                if len(price_info)==1:
                    msrp=float(price_info[0].strip("$").replace(",",""))
                    product_info['msrp']=msrp
                elif len(price_info)==2:
                    msrp=float(price_info[1].strip("$").replace(",",""))
                    sale=float(price_info[0].strip("$").replace(",",""))
                    product_info['msrp']=msrp
                    product_info['sale']=sale
                else:
                    print('WARNING')

                print(product_info)

                # for t in product.find_all('dd'):
                #     ttext = t.text
                #     print(t.text)

                #     if (len(ttext)>0) and ('$' in ttext):
                #         splittext = ttext.split('MSRP: ')
                #         print(splittext)
                #         if len(splittext)==2:
                #             sale=splittext[0]
                #             msrp=splittext[1]
                #         elif len(splittext)==1:
                #             msrp=splittext[0]
                #             

                print("\nMSRP={}\nSALE={}\n".format(msrp,sale))
                url_end = product.find("a",attrs={"itemprop":"url"}).attrs['href']
                product_url = "https://www.zappos.com" + url_end
                print('\n product url' + '\n' + product_url)
                split_url = url_end.split('/') 
                product_sku = split_url[split_url.index("product")+1]
                product_color = split_url[split_url.index("color")+1]

                # product_sku = split_url[6]
                # product_color = split_url[8]
                print('SKU: {}\nColor: {}\n'.format(product_sku,product_color))
                product_details = [ product_url, msrp, sale ] 
                self.product_list.append(product_details)
                #skus_id.append(product_sku)
                #colors_id.append(product_color)

    def print_product_list(self):
        print("in print_product_list")
        if self.product_list is None:
            self.get_product_list()
        if self.product_list is not None:
            print("======== Like Product URLs  ========\n")
            for i,prod in enumerate(self.product_list):
                print("*** Product #{} ***".format(i))
                for detail,name in zip(prod,['url:   ','msrp:  ','sale:  ']):
                    print("{}\t{}".format(name,detail))
                print("*******************\n".format(i))
            print("\n====================================")
    def get_search_page_dict(self):
        if self.product_list is None:
            self.get_product_list
        if self.product_list is not None:
            self.product_dict = dict()
            # product = [url,msrp,sale]
            #for product in self.product_list[0:5]:
            for count, product in enumerate(self.product_list):
                print("\nProduct #{}".format(count))
                print(product)
                self.product_dict[product[0]] = dict()
                self.product_dict[product[0]]['msrp'] = product[1]
                self.product_dict[product[0]]['sale'] = product[2]

                # get ParseProduct object which holds 
                # all info about product. Makes a call with Selenium with Chrome Driver---REMEMBER
                # to Obfuscate this either with TOR or something else
                #parsed_product = ParseProduct('https://www.zappos.com/p/cole-haan-original-grand-shortwing-woodbury-leather-java/product/8931778/color/646844')
                parsed_product = ParseProduct(product[0])
                if parsed_product.bad_link == True:
                    continue
                else:

                    # add details to dictionary entry 
                    #self.product_details = [self.category,self.subcategory,self.brand,self.name,self.color]
                    parsed_product_details =  parsed_product.get_product_details()
                    parsed_product.print_product_details()
                    self.product_dict[product[0]]['category'] =parsed_product_details[0] 
                    self.product_dict[product[0]]['subcategory'] =parsed_product_details[1] 
                    self.product_dict[product[0]]['brand'] =parsed_product_details[2] 
                    self.product_dict[product[0]]['name'] =parsed_product_details[3] 
                    self.product_dict[product[0]]['color'] =parsed_product_details[4] 


                    #like_product = [url,msrp,sale]
                    #self.like_products.append(like_product)
                    parsed_product_like_products =  parsed_product.get_like_products()
                    if parsed_product.like_products_exist:
                        self.product_dict[product[0]]['like_products'] = dict()
                        for like_product in parsed_product_like_products:
                            self.product_dict[product[0]]['like_products'][like_product[0]] = dict()
                            self.product_dict[product[0]]['like_products'][like_product[0]]['msrp'] = like_product[1]
                            self.product_dict[product[0]]['like_products'][like_product[0]]['sale'] = like_product[2]
                    else:
                        self.product_dict[product[0]]['like_products'] = None

                    parsed_product_image_urls =  parsed_product.get_image_urls()
                    self.product_dict[product[0]]['image_urls'] = parsed_product_image_urls
                    
                    #product.print_product_details()
                    #print(product.get_image_urls())
                    #product.print_like_products()




            if (self.page is not None) and (self.subcategory is not None):
                filename = 'data/{}_p{}.json'.format(self.subcategory,self.page)
            else:
                filename = 'data/data.json'

            with open(filename, 'w') as fp:
                json.dump(self.product_dict, fp, sort_keys=True, indent=4)
            return self.product_dict



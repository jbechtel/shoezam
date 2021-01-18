from enum import Enum
import re
import attr
from attr.validators import instance_of, optional, in_, deep_iterable
import typing as T
from bs4 import BeautifulSoup
# import requests
# import os
# import gevent
from random import randint
from .Misc import get_page
from .ParseProduct import ParseProduct
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
from dataclasses import dataclass

import logging
logger = logging.getLogger(__name__)

_SEARCH_PAGE_BASE_URL = "https://www.zappos.com/{}-{}/.zso?t=men%20{}&p={}" # .format(Gender, ShoeType, ShoeType, page_num)

class Gender(Enum):
    MEN = 'men'
    WOMEN = 'women'
    KIDS = 'kids'

class ShoeType(Enum):
    OXFORDS = 'oxfords'
    SNEAKER = 'sneakers-athletic-shoes'


@attr.s
class ProductDetails:
    """ Keeps track of Product URL, msrp & sale prices
    """
    url: str = attr.ib(validator=instance_of(str))
    sku: int = attr.ib(validator=instance_of(int))
    msrp: float = attr.ib(validator=instance_of(float))
    category: str = attr.ib(validator=instance_of(str))
    subcategory: str = attr.ib(validator=instance_of(str))
    brand: str = attr.ib(validator=instance_of(str))
    name: str = attr.ib(validator=instance_of(str))
    color: str = attr.ib(validator=instance_of(str))
    colorID: int = attr.ib(validator=instance_of(int))
    brandID: int = attr.ib(validator=instance_of(int))
    productID: int = attr.ib(validator=instance_of(int))
    styleID: int = attr.ib(validator=instance_of(int))
    sale: T.Optional[float] = attr.ib(validator=optional(instance_of(float)),
                                      default=None)
    like_products_urls: T.Optional[T.List[str]] = attr.ib(validator=optional(
        deep_iterable(instance_of(str), instance_of(T.Sequence))), init=False,
        default=None)
    image_urls: T.Optional[T.List[str]] = attr.ib(validator=optional(
        deep_iterable(instance_of(str), instance_of(T.Sequence))), init=False,
        default=None)

    @staticmethod
    def soup(url: str) -> BeautifulSoup:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        wait_time = randint(4, 8)
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, 'alsoLike')))
        except TimeoutException as e:
            print(f'Page timed out after {wait_time} secs.')
            raise e
        source = driver.page_source
        driver.quit()
        soup = BeautifulSoup(source, 'html.parser')
        assert soup.find('body', class_="activeMain") is not None, f'Bad link {url}'
        return soup



    @classmethod
    def from_url(cls, url: str) -> 'ProductDetails':
        soup = ProductDetails.soup(url)
        price_data = soup.find(text=re.compile("originalPrice"))
        price_data = price_data.string.split('window.__INITIAL_STATE__ =')[1][0:-1]
        price_dict = json.loads(price_data)
        detail_dict = dict()
        detail_dict['brandID'] = price_dict['product']['detail']['brandId']
        detail_dict['productID'] = price_dict['product']['detail']['productId']
        detail_dict['productName'] = price_dict['product']['detail']['productName']
        detail_dict['brandName'] = price_dict['product']['detail']['brandName']
        detail_dict['sku'] = price_dict['pixelServer']['data']['product']['sku']
        detail_dict['styleID'] = price_dict['pixelServer']['data']['product']['styleId']
        detail_dict['price'] = price_dict['pixelServer']['data']['product']['price']
        detail_dict['oprice'] = price_dict['pixelServer']['data']['product'].get('originalPrice',None)
        detail_dict['name'] = price_dict['pixelServer']['data']['product']['name']
        detail_dict['brand'] = price_dict['pixelServer']['data']['product']['brand']
        detail_dict['category'] = price_dict['pixelServer']['data']['product']['category']
        detail_dict['subcategory'] = price_dict['pixelServer']['data']['product']['subCategory']

        for style in price_dict['product']['detail']['styles']:
            if style['styleId'] == detail_dict['styleID']:
                detail_dict['color'] = style['color']
                detail_dict['colorID'] = style['colorId']
                detail_dict['style_price'] = style['price']
                detail_dict['style_oprice'] = style['originalPrice']
                break
        sale = float(detail_dict['style_price'].strip('$'))
        msrp = float(detail_dict['style_price'].strip('$'))
        category = detail_dict['category']
        subcategory = detail_dict['subcategory']
        name = detail_dict['name']
        brand = detail_dict['brand']
        color = detail_dict['color']
        colorID = int(detail_dict['colorID'])
        styleID = int(detail_dict['styleID'])
        productID = int(detail_dict['productID'])
        brandID = int(detail_dict['brandID'])
        sku = int(detail_dict['sku'])

        if abs(sale-msrp) < 0.01:
            sale = None

        logger.debug(detail_dict)
        return cls(url=url, sku=sku, msrp=msrp, sale=sale, category=category,
                   subcategory=subcategory, brand=brand, name=name, color=color,
                   colorID=colorID, styleID=styleID, productID=productID,
                   brandID=brandID)


# class ParseProduct(object):
#     """ parses html product info scraped from Zappos
#
#     Args:
#         html: html from product URL
#         url: product URL
#     Attributes:
#         asdf
#
#     """
#
#     def __init__(self, url, price=None):
#
#         # like_products urls will be 4 recommended product urls
#         # [ url0, url1, ...]
#         self.like_products = None
#
#         # image_urls will be 5 urls to 5 jpgs
#         # [ url0, url1, ...]
#         self.image_urls = None
#         if self.bad_link == False:
#             self.get_product_details()
#             self.get_image_urls()
#             # LIKE PRODUCTS MAY NOT EXIST!
#             if self.like_products_exist:
#                 self.get_like_products()
#
#     def get_like_products(self):
#         if self.like_products is not None:
#             return self.like_products
#         elif self.like_products_exist:
#             # alsoLike = self.soup.find('body',class_="activeMain").find('div',attrs={'id':'alsoLike'}).find_all('a',# attrs={'data-type':'You May Also Like'})
#             # alsoLike = self.soup.find('div',attrs={'id':'root'}).find_all('a',attrs={'data-type':'You May Also Like'})
#
#             alsoLike = self.soup.find('div', attrs={'id': 'alsoLike'}).find_all(
#                 'a', {'data-type': 'You May Also Like'})
#             # alsoLike = self.soup.find('div',attrs={'id':'root'}).find('div',attrs={'id':'productRecap'}).find_all('div',# attrs={'id':'itemInformation'})
#             # print('alsoLike: {}'.format(alsoLike))
#             self.like_products = []
#             for i, item in enumerate(alsoLike):
#                 url_end = item.attrs['href']
#                 clipped_end = url_end.split('?', 1)[0]
#                 url = "https://www.zappos.com" + clipped_end
#                 # print(url)
#                 all_text = [t.text for t in item.find_all('span')]
#                 # print(all_text)
#                 sale = None
#                 # print('len all_text: {}'.format(len(all_text)))
#                 if len(all_text) == 7:
#                     # msrp with dollar sign str
#                     msrp = all_text[-1]
#                     # sale with dollar sign str
#                     sale = all_text[-3]
#                 elif len(all_text) == 5:
#                     msrp = all_text[-1]
#                 like_product = [url, msrp, sale]
#                 self.like_products.append(like_product)
#             return self.like_products
#
#     def print_like_products(self):
#         print("in print_product_details")
#         if (self.like_products is None) and (self.like_products_exist):
#             self.get_like_products()
#         if self.like_products is not None:
#             print("======== Like Product URLs  ========\n")
#             for i, prod in enumerate(self.like_products):
#                 print("\n*** Product #{} ***".format(i))
#                 for detail, name in zip(prod,
#                                         ['url:   ', 'msrp:  ', 'sale:  ']):
#                     print("{}\t{}".format(name, detail))
#                 print("*******************".format(i))
#             print("\n====================================")
#         else:
#             print("\n NO Like Products exist...\n")
#
#     def get_image_urls(self):
#         print("in get_image_urls")
#         if self.image_urls is not None:
#             print("self.iimage_urls is not None")
#             return self.image_urls
#         else:
#             print("In else")
#             print(f'self.soup: {self.soup.prettify()}')
#             thumbs = self.soup.find('body', class_="activeMain jsEnabled").find(
#                 'ul', attrs={'id': 'thumbnailsList'})
#             print(f'thumbs: {thumbs.prettify()}')
#             small_urls = []
#
#             pair = thumbs.find('img', attrs={'alt': 'PAIR'})
#             if pair is not None:
#                 small_pair_url = pair.attrs['src']
#                 small_urls.append(small_pair_url)
#
#             top = thumbs.find('img', attrs={'alt': 'TOPP'})
#             if top is not None:
#                 small_top_url = top.attrs['src']
#                 small_urls.append(small_top_url)
#
#             left = thumbs.find('img', attrs={'alt': 'LEFT'})
#             if left is not None:
#                 small_left_url = left.attrs['src']
#                 small_urls.append(small_left_url)
#
#             right = thumbs.find('img', attrs={'alt': 'RGHT'})
#             if right is not None:
#                 small_right_url = right.attrs['src']
#                 small_urls.append(small_right_url)
#
#             pair = thumbs.find('img', attrs={'alt': 'FRNT'})
#             print('pair = {}'.format(pair))
#             if pair is not None:
#                 print('pair is not None')
#                 small_pair_url = pair.attrs['src']
#                 print('small_pair_url: {}'.format(small_pair_url))
#                 small_urls.append(small_pair_url)
#             # small_urls = [ small_pair_url, small_top_url, small_left_url, small_right_url ]
#             # print('small_urls: {}'.format(small_urls))
#             big_urls = []
#             for url in small_urls:
#                 big_url = url.replace('_SR106,78_', '_SX480_')
#                 big_urls.append(big_url)
#             self.image_urls = big_urls
#             return self.image_urls
#
#     def get_product_details(self):
#         # print("in get_product_details")
#         if self.product_details is not None:
#             return self.product_details
#         else:
#             header_data = self.soup.find('body', class_="activeMain").find(
#                 'div', attrs={'id': 'breadcrumbs'}).find_all(
#                 'a')  # ('div',class_='SRGgm')
#             for i, head in enumerate(header_data):
#                 # print('text #{}'.format(i) + head.text)
#                 if i == 1:
#                     # print('appending: {}'.format(head.text))
#                     self.category = head.text
#                 elif i == 2:
#                     # print('appending: {}'.format(head.text))
#                     self.subcategory = head.text
#                 elif i == 3:
#                     # print('appending: {}'.format(head.text))
#                     self.brand = head.text
#
#             # brand_data = self.soup.find('body',class_="activeMain").find('span',attrs={'itemprop':'brand'}).find_all('a')#('div',# class_='SRGgm')
#             # print(brand_data)
#             # brand = brand_data.text
#             # name_data = self.soup.find('body',class_="activeMain").find('meta',attrs={'itemprop':'name'}).find_all('a')
#             # name_data = self.soup.find('body',class_="activeMain").find_all('meta',attrs={'itemprop':'name'})
#             # print(name_data)
#             # self.name = name_data.attrs['content']
#             name_data = self.soup.find('head').find('title').text.split()
#             # print(name_data.text.split())
#             # print(name_data)
#             name = name_data[len(self.brand.split()):-2]
#             self.name = " ".join(name)
#             # print(self.name)
#             color_data = self.soup.find('body', class_="activeMain").find(
#                 'meta', attrs={'itemprop': 'color'})
#             self.color = color_data.attrs['content']
#             # print('self.color: {}'.format(self.color))
#
#             # price_data = self.soup.find('body',class_="activeMain").find('div',attrs={'id':'stage'})
#             # print(price_data)
#             # price_text = self.text
#             # print(price_text)
#             self.product_details = [self.category, self.subcategory, self.brand,
#                                     self.name, self.color]
#             return self.product_details
#
#     def print_product_details(self):
#         print("in print_product_details")
#         if self.product_details is None:
#             self.get_product_details()
#         if self.product_details is not None:
#             print("======== Product Details ========\n")
#             for detail, name in zip(self.product_details,
#                                     ['category:   ', 'subcategory:',
#                                      'brand:      ', 'name:       ',
#                                       'color:      ']):
#                 print("{}\t{}".format(name, detail))
#             print("\n=================================")


@attr.s
class SearchPage:
    gender: Gender = attr.ib(validator=instance_of(Gender))
    shoe_type: ShoeType = attr.ib(validator=instance_of(ShoeType))
    page: int = attr.ib(validator=instance_of(int))
    url_base: T.Optional[str] = attr.ib(validator=instance_of(str),
                                        default=_SEARCH_PAGE_BASE_URL,
                                        kw_only=True)

    @property
    def url(self):
        url = self.url_base.format(self.gender.value,
                                   self.shoe_type.value,
                                   self.shoe_type.value,
                                   self.page)
        logger.debug(f'SearchPage URL: {url}')
        return url

    @property
    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(get_page(self.url), 'html.parser')

    def parse_product_urls(self) -> T.List[str]:
        soup = self.soup
        outer = soup.find("div", attrs={"class": "searchPage"})
        product_urls = []
        for i, product in enumerate(outer.find_all("article")):
            url_end = product.find("a", attrs={"itemprop": "url"}).attrs['href']
            product_url = "https://www.zappos.com" + url_end
            logger.debug(f'product url: {product_url}')
            product_urls.append(product_url)
        return product_urls

    def parse_products(self) -> T.List[ProductDetails]:
        return [ProductDetails.from_url(x) for x in self.parse_product_urls()]






# class ParseSearch(object):
#     """ parses html search page info scraped from Zappos
#
#     Args:
#         html: html from product URL
#         url: product URL
#
#     """
#
#     def __init__(self, url,page=None,subcategory=None):
#         if page is not None:
#             self.page = page
#         if subcategory is not None:
#             self.subcategory = subcategory
#         product_page = get_page(url)
#         self.soup = BeautifulSoup(product_page, 'html.parser')
#         # print(self.soup)
#
#         #driver = webdriver.Chrome()
#         #driver.get(url)
#         #try:
#         #    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'alsoLike')))
#         #except TimeoutException:
#         #    print('Page timed out after 10 secs.')
#         #self.soup = BeautifulSoup(driver.page_source, 'html.parser')
#         #driver.quit()
#
#
#         # product_urls list of urls and price for each product on the page
#         #
#         self.product_list = None
#         self.get_product_list()
#     def get_product_list(self):
#         """
#
#         :return:
#         """
#         if self.product_list is not None:
#             return self.product_list
#         else:
#             self.product_list = []
#             outer = self.soup.find("div",attrs={"class":"searchPage"})
#             for i,product in enumerate(outer.find_all("article")):
#                 print(product.prettify())
#                 # name_soup = product.find('p',attrs={'itemprop':'name'})
#                 # name_soup = product.find('dl',attrs={'itemprop':'name'})
#                 name_soup = product.find('dd', attrs={'itemprop': 'name'})
#                 print(f'\n\ndd: {name_soup.prettify()}')
#                 name = name_soup.text
#                 print("NAME: {}".format(name))
#                 print('\n\n')
#                 #print('\n product #{}'.format(i))
#                 #all_text = [t.text for t in product.find_all('p')
#                 color_soup = product.find('dd', attrs={'itemprop': 'color'})
#                 print(f'\n\ndd: {color_soup.prettify()}')
#                 color = color_soup.text
#                 print("COLOR: {}".format(color))
#                 print('\n\n')
#                 brand_soup = product.find('dd', attrs={'itemprop': 'brand'})
#                 print(f'\n\ndd: {brand_soup.prettify()}')
#                 brand = brand_soup.text
#                 print("BRAND: {}".format(brand))
#                 print('\n\n')
#
#                 price_soup = product.find('dd', attrs={'itemprop': 'offers'})
#                 print(f'\n\ndd: {price_soup.prettify()}')
#                 price_info = price_soup.text.split('MSRP: ')
#                 print("PRICE: {}".format(price_info))
#                 print('\n\n')
#
#                 msrp = None
#                 sale = None
#                 # pi = [t.text for t in product.find_all('dd')]
#
#                 product_info = {'brand': brand, 'name': name, 'color': color}
#                 # price_info = pi[3].split('MSRP: ')
#                 if len(price_info)==1:
#                     msrp=float(price_info[0].strip("$").replace(",",""))
#                     product_info['msrp']=msrp
#                 elif len(price_info)==2:
#                     msrp=float(price_info[1].strip("$").replace(",",""))
#                     sale=float(price_info[0].strip("$").replace(",",""))
#                     product_info['msrp']=msrp
#                     product_info['sale']=sale
#                 else:
#                     print('WARNING')
#
#                 print(product_info)
#
#                 # for t in product.find_all('dd'):
#                 #     ttext = t.text
#                 #     print(t.text)
#
#                 #     if (len(ttext)>0) and ('$' in ttext):
#                 #         splittext = ttext.split('MSRP: ')
#                 #         print(splittext)
#                 #         if len(splittext)==2:
#                 #             sale=splittext[0]
#                 #             msrp=splittext[1]
#                 #         elif len(splittext)==1:
#                 #             msrp=splittext[0]
#                 #
#
#                 print("\nMSRP={}\nSALE={}\n".format(msrp,sale))
#                 url_end = product.find("a",attrs={"itemprop":"url"}).attrs['href']
#                 product_url = "https://www.zappos.com" + url_end
#                 print('\n product url' + '\n' + product_url)
#                 split_url = url_end.split('/')
#                 product_sku = split_url[split_url.index("product")+1]
#                 product_color = split_url[split_url.index("color")+1]
#
#                 # product_sku = split_url[6]
#                 # product_color = split_url[8]
#                 print('SKU: {}\nColor: {}\n'.format(product_sku,product_color))
#                 product_details = ProductDetails(url=product_url, msrp=msrp,
#                                                  sale=sale)
#
#                 self.product_list.append(product_details)
#                 #skus_id.append(product_sku)
#                 #colors_id.append(product_color)
#
#     def print_product_list(self):
#         print("in print_product_list")
#         if self.product_list is None:
#             self.get_product_list()
#         if self.product_list is not None:
#             print("======== Like Product URLs  ========\n")
#             for i,prod in enumerate(self.product_list):
#                 print("*** Product #{} ***".format(i))
#                 print(prod)
#                 print("*******************\n".format(i))
#             print("\n====================================")
#     def get_search_page_dict(self):
#         """
#
#         :return: dict
#         """
#         if self.product_list is None:
#             self.get_product_list
#         if self.product_list is not None:
#             self.product_dict = dict()
#             # product = [url,msrp,sale]
#             #for product in self.product_list[0:5]:
#             for count, product in enumerate(self.product_list):
#                 print("\nProduct #{}".format(count))
#                 print(product)
#                 self.product_dict[product.url] = dict()
#                 self.product_dict[product.url]['msrp'] = product.msrp
#                 self.product_dict[product.url]['sale'] = product.sale
#
#                 # get ParseProduct object which holds
#                 # all info about product. Makes a call with Selenium with Chrome Driver---REMEMBER
#                 # to Obfuscate this either with TOR or something else
#                 #parsed_product = ParseProduct('https://www.zappos.com/p/cole-haan-original-grand-shortwing-woodbury-leather-java# /product/8931778/color/646844')
#                 parsed_product = ParseProduct(product.url)
#                 if parsed_product.bad_link == True:
#                     continue
#                 else:
#
#                     # add details to dictionary entry
#                     #self.product_details = [self.category,self.subcategory,self.brand,self.name,self.color]
#                     parsed_product_details = parsed_product.get_product_details()
#                     parsed_product.print_product_details()
#                     self.product_dict[product[0]]['category'] =parsed_product_details[0]
#                     self.product_dict[product[0]]['subcategory'] =parsed_product_details[1]
#                     self.product_dict[product[0]]['brand'] =parsed_product_details[2]
#                     self.product_dict[product[0]]['name'] =parsed_product_details[3]
#                     self.product_dict[product[0]]['color'] =parsed_product_details[4]
#
#
#                     #like_product = [url,msrp,sale]
#                     #self.like_products.append(like_product)
#                     parsed_product_like_products =  parsed_product.get_like_products()
#                     if parsed_product.like_products_exist:
#                         self.product_dict[product[0]]['like_products'] = dict()
#                         for like_product in parsed_product_like_products:
#                             self.product_dict[product[0]]['like_products'][like_product[0]] = dict()
#                             self.product_dict[product[0]]['like_products'][like_product[0]]['msrp'] = like_product[1]
#                             self.product_dict[product[0]]['like_products'][like_product[0]]['sale'] = like_product[2]
#                     else:
#                         self.product_dict[product[0]]['like_products'] = None
#
#                     parsed_product_image_urls =  parsed_product.get_image_urls()
#                     self.product_dict[product[0]]['image_urls'] = parsed_product_image_urls
#
#                     #product.print_product_details()
#                     #print(product.get_image_urls())
#                     #product.print_like_products()
#
#
#
#
#             if (self.page is not None) and (self.subcategory is not None):
#                 filename = 'data/{}_p{}.json'.format(self.subcategory,self.page)
#             else:
#                 filename = 'data/data.json'
#
#             with open(filename, 'w') as fp:
#                 json.dump(self.product_dict, fp, sort_keys=True, indent=4)
#             return self.product_dict
#

def gen_dict_extract(key: str, var: T.Dict):
    if hasattr(var,'iteritems'):
        for k, v in var.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

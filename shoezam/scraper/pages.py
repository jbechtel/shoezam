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
from .data_classes import ProductDetails
from .enums import Gender, ShoeType
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
from dataclasses import dataclass

import logging

logger = logging.getLogger(__name__)

MIN_WAIT_TIME = 1
_SEARCH_PAGE_BASE_URL = "https://www.zappos.com/{}-{}/.zso?t=men%20{}&p={}"  # .format(Gender, ShoeType, ShoeType, page_num)


@attr.s
class ProductPage:
    """ Keeps track of Product URL
    """
    url: str = attr.ib(validator=instance_of(str))
    like_products_urls: T.Optional[T.List[str]] = attr.ib(validator=optional(
        deep_iterable(instance_of(str), instance_of(T.Sequence))), init=False,
        default=None)
    image_urls: T.Optional[T.List[str]] = attr.ib(validator=optional(
        deep_iterable(instance_of(str), instance_of(T.Sequence))), init=False,
        default=None)
    soup: T.Optional[BeautifulSoup] = attr.ib(
        validator=optional(instance_of(BeautifulSoup)), init=False,
        default=None)

    def _get_soup(self) -> BeautifulSoup:
        if self.soup is None:
            self.soup = self.get_product_page_soup(self.url)
        return self.soup

    @staticmethod
    def get_product_page_soup(url: str) -> BeautifulSoup:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        wait_time = randint(MIN_WAIT_TIME, MIN_WAIT_TIME+3)
        logger.info(f'wait_time: {wait_time}')
        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, 'alsoLike')))
        except TimeoutException as e:
            logger.info(f'Page timed out after {wait_time} secs.')
            raise e
        source = driver.page_source
        driver.quit()
        soup = BeautifulSoup(source, 'html.parser')
        assert soup.find('body', class_="activeMain") is not None, f'Bad link {url}'
        return soup

    def get_product_details(self) -> ProductDetails:
        soup = self._get_soup()
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
        detail_dict['oprice'] = price_dict['pixelServer']['data']['product'].get('originalPrice', None)
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

        if abs(sale - msrp) < 0.01:
            sale = None

        logger.debug(detail_dict)
        like_product_urls = [page.url for page in self.get_like_product_pages()]
        image_urls = self.get_image_urls()
        return ProductDetails(url=self.url, sku=sku, msrp=msrp, sale=sale,
                              category=category,
                              subcategory=subcategory, brand=brand, name=name,
                              color=color,
                              colorID=colorID, styleID=styleID,
                              productID=productID,
                              brandID=brandID,
                              like_product_urls=like_product_urls,
                              image_urls=image_urls
                              )

    def get_like_product_pages(self) -> T.List['ProductPage']:
        """

        :return:
        """
        soup = self._get_soup()
        also_like = soup.find('div', attrs={'id': 'alsoSimilar'}).find_all('article', attrs={'itemtype': 'http://schema.org/Product'})
        like_product_pages = []
        for i, item in enumerate(also_like):
            url_end = item.find(href=True)['href']
            clipped_end = url_end.split('?', 1)[0]
            url = "https://www.zappos.com" + clipped_end
            like_product = ProductPage(url=url)
            like_product_pages.append(like_product)
        logger.debug(like_product_pages)
        return like_product_pages

    def get_image_urls(self) -> T.Dict[str, str]:
        soup = self._get_soup()
        thumbs = soup.find('body', class_="activeMain jsEnabled").find('ul', attrs={'id': 'thumbnailsList'})
        image_urls = {x['aria-label'].replace(' ', '_'): x['href'].replace('_SR106,78', '_SX480_') for x in thumbs.find_all(href=True)}
        logger.debug(image_urls)
        return image_urls


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

    def parse_product_pages(self) -> T.List[ProductPage]:
        soup = self.soup
        outer = soup.find("div", attrs={"class": "searchPage"})
        product_pages = []
        for i, product in enumerate(outer.find_all("article")):
            url_end = product.find("a", attrs={"itemprop": "url"}).attrs['href']
            product_url = "https://www.zappos.com" + url_end
            logger.debug(f'product url: {product_url}')
            product_pages.append(ProductPage(product_url))
        return product_pages


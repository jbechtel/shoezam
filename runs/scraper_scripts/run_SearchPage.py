from shoezam.scraper.pages import SearchPage, ProductPage
from shoezam.scraper.enums import Gender, ShoeType
from shoezam.scraper.data_classes import ProductDetails
import logging

logger = logging.getLogger('shoezam.scraper')
logger.setLevel(logging.DEBUG)
page = 0

# search_page = SearchPage(gender=Gender.MEN,
#                          shoe_type=ShoeType.OXFORDS,
#                          page=page)
# product_urls = search_page.parse_product_urls()

url='https://www.zappos.com/p/trask-rogan-navy-italian-calfskin/product/9281120/color/435399'
logger.info(url)
page = ProductPage(url=url)
product_details = page.get_product_details()
logger.info(product_details)
like_product_pages = page.get_like_product_pages()
logger.info(like_product_pages)
image_urls = page.get_image_urls()
logger.info(image_urls)







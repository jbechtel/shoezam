from shoezam.scraper.ParseSearch import SearchPage, Gender, ShoeType, ProductDetails
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
product_details = ProductDetails.from_url(url=url)
logger.info(product_details)







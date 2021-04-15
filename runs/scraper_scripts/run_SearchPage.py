from shoezam.scraper.pages import SearchPage, ProductPage
from shoezam.scraper.enums import Gender, ShoeType
from shoezam.scraper.data_classes import ProductDetails
from shoezam.scraper.images import ImageDownloader, dataIO
import logging

logger = logging.getLogger('shoezam.scraper')
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
page_num = 0

# search_page = SearchPage(gender=Gender.MEN,
#                          shoe_type=ShoeType.OXFORDS,
#                          page=page)
# product_urls = search_page.parse_product_urls()

url='https://www.zappos.com/p/trask-rogan-navy-italian-calfskin/product/9281120/color/435399'
logger.info(url)
page = ProductPage(url=url)
pages = page.get_like_product_pages()
product_details = page.get_product_details()
logger.info(product_details)
like_product_pages = page.get_like_product_pages()
logger.info(like_product_pages)
image_urls = page.get_image_urls()
logger.info(image_urls)
logger.info(product_details.image_urls)

crawler = ImageDownloader()
images = crawler.get_product_images(product_details)
logger.info(images.keys())
io = dataIO()
io.save_images(images, product_details)






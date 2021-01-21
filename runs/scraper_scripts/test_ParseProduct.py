#from zap_scrap import ParseProduct.ParseProduct
from shoezam import zap_scrap as zs

product = zs.ParseProduct('https://www.zappos.com/p/cole-haan-original-grand-shortwing-woodbury-leather-java/product/8931778/color/646844')
product.print_product_details()
print(product.get_image_urls())
product.print_like_products()

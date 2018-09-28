#from zap_scrap import ParseProduct.ParseProduct
import zap_scrap as zs

#url = "https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=goliveRecentSalesStyle/desc/&p=" + str(i)
url = "https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=goliveRecentSalesStyle/desc"
url = "https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=goliveRecentSalesStyle/desc/&p=1"
url = "https://www.zappos.com/men-oxfords/CK_XARC31wHAAQLiAgMBAhg.zso"
page = 0
subcategory = 'oxfords'
url = "https://www.zappos.com/men-oxfords/CK_XARC31wHAAQLiAgMBAhg.zso?p=" + str(page)
search_page = zs.ParseSearch(url,page,subcategory)
search_page.print_product_list()
search_page.get_search_page_dict()

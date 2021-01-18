import zap_scrap as zs

for i in range(1,24):
    page = i
    subcategory = 'oxfords'
    db_filename = subcategory + '_p{}.json'.format(page)
    data_dir = './data/' 
    image_dir = './images/'
    crawler = zs.ImageCrawler(data_dir, image_dir, db_filename)

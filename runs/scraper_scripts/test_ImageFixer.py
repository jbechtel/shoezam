import zap_scrap as zs


data_dir = './databases/oxfords_db.json' 
image_dir = './images/'
crawler = zs.ImageFixer.ImageFixer(data_dir, image_dir)

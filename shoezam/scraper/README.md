# zap_scrap

zap_scrap is a web scraper built with Selenium and BeautifulSoup that allows users to collect product info and images from zappos. 

The process is broken up into several parts. First the product info, and image urls are collected using the `ParseSearch(url,page,subcategory)` class where `url` is a string for a product search page on zappos, `page` is the page of the search results, and `subcategory` is the type of product i.e. shoe boot oxford etc. The meta data is collected via
```
import zap_scrap as zs
subcategory = 'oxfords'
page = 0
url = "https://www.zappos.com/men-oxfords/CK_XARC31wHAAQLiAgMBAhg.zso?p=" + str(page)
search_page = zs.ParseSearch(url,page,subcategory)
search_page.print_product_list()
search_page.get_search_page_dict()
```

This stores each product as a dictionary entry in the subdirectory `"data/{}_p{}.json".format(subcategory,page)` where an example entry looks like:
```
    "https://www.zappos.com/p/allen-edmonds-bond-street-black/product/9113612/color/3": {
        "brand": "Allen Edmonds",
        "category": "Shoes",
        "color": "Black",
        "image_urls": [
            "https://m.media-amazon.com/images/I/61ak0lDU+oL._SX480_.jpg",
            "https://m.media-amazon.com/images/I/71czISPgDSL._SX480_.jpg",
            "https://m.media-amazon.com/images/I/61JMxvDItoL._SX480_.jpg",
            "https://m.media-amazon.com/images/I/61VHGP+JiJL._SX480_.jpg"
        ],
        "like_products": {
            "https://www.zappos.com/p/deer-stags-cyprus-black-black/product/9110306/color/183092": {
                "msrp": "$65.00",
                "sale": "$45.00"
            },
            "https://www.zappos.com/p/kenneth-cole-new-york-levin-lace-up-black/product/9100169/color/3": {
                "msrp": "$160.00",
                "sale": null
            },
            "https://www.zappos.com/p/to-boot-new-york-grant-black-plc/product/8284088/color/469987": {
                "msrp": "$395.00",
                "sale": null
            }
        },
        "msrp": "$425.00",
        "name": "Bond Street",
        "sale": null,
        "subcategory": "Oxfords"
    },
```
In this dictionary the keys are the product url, and the values hold another dictionary with all meta data.

Next, the `ImageCrawler` class can be used to download images as follows. Working from the above example
```
db_filename = subcategory + '_p{}.json'.format(page)
data_dir = './data/' 
image_dir = './images/'
crawler = zs.ImageCrawler(data_dir, image_dir, db_filename)
```
Images get stored as jpgs in directories named according to `"{}/{}_product_{}_color_{}.format(image_dir,subcategory,product_key,color_key)"` where `product_key` and `color_key` are unique identifiers for the products.

Once images are collected a database can be made using the `dataIO.compile_database(save_dir,category)` where `save_dir` is where to save the compiled database and `category` is the product type.
```
category = 'oxfords'
save_dir = 'databases'
zs.dataIO.compile_database(save_dir, category)
```
In this example, `dataIO.compile_database()` looks for all jsons in `"./data/{}_*".format(category)"` and combines them into one database where an example entry is as follows: 
```
    "boats_product_104678_color_310": {
        "brand": "Sebago",
        "category": "Shoes",
        "color": "Cognac Leather",
        "image_paths": [
            "/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_boats/boats_product_104678_color_310/boats_product_104678_color_310_0.jpg",
            "/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_boats/boats_product_104678_color_310/boats_product_104678_color_310_1.jpg",
            "/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_boats/boats_product_104678_color_310/boats_product_104678_color_310_2.jpg",
            "/Users/bechtel/Work/Insight/shoezam/zap_scrap/scripts/images_boats/boats_product_104678_color_310/boats_product_104678_color_310_3.jpg"
        ],
        "image_urls": [
            "https://m.media-amazon.com/images/I/81CCtVEvk6L._SX480_.jpg",
            "https://m.media-amazon.com/images/I/81TYx8RBPqL._SX480_.jpg",
            "https://m.media-amazon.com/images/I/81vIIlAJM5L._SX480_.jpg",
            "https://m.media-amazon.com/images/I/81nz3Ui+bnL._SX480_.jpg"
        ],
        "like_product_keys": [
            "boats_product_8806685_color_662572",
            "boats_product_8982426_color_621",
            "boats_product_8982442_color_6",
            "boats_product_9033991_color_20"
        ],
        "like_products": {
            "https://www.zappos.com/p/columbia-super-bonehead-vent-leather-pfg2-elk-curry/product/8806685/color/662572": {
                "msrp": "$110.00",
                "sale": null
            },
            "https://www.zappos.com/p/sperry-gold-a-o-2-eye-crepe-suede-sand/product/8982426/color/621": {
                "msrp": "$170.00",
                "sale": "$119.99"
            },
            "https://www.zappos.com/p/sperry-gold-gamefish-3-eye-brown/product/8982442/color/6": {
                "msrp": "$169.95",
                "sale": null
            },
            "https://www.zappos.com/p/tommy-hilfiger-bowman-tan/product/9033991/color/20": {
                "msrp": "$80.00",
                "sale": "$69.99"
            }
        },
        "msrp": "$130.00",
        "name": "Schooner",
        "sale": null,
        "subcategory": "Boat Shoes",
        "url": "https://www.zappos.com/p/sebago-schooner-cognac-leather/product/104678/color/310"
```
The keys have been converted to a more useful format similar to the `image_dir` names as specified above. The database is stored to `"./{}/{}_db.json".format(save_dir,subcategory)`. 

Sometimes images fail to download, and in this case the `ImageFixer` class can be used. Continuing with the above example, the following code will search through the database as well as the image urls, checking whether each picture has been succesfully downloaded.
```
data_dir = './databases/oxfords_db.json' 
image_dir = './images/'
crawler = zs.ImageFixer.ImageFixer(data_dir, image_dir)
```



from bs4 import BeautifulSoup
import requests
import os
import gevent

product_names = []
product_urls = []
img_urls = []
category = []
subcategory = []
brand = []
skus_id = []
styles_id = []
colors_id = []


def main():
    os.chdir('./test_images')
    for i in range (0, 1):
        url = "http://www.zappos.com/mens-sneakers-athletic-shoes~dA?zfcTest=sis%3A0#!/men-sneakers-athletic-shoes-page2/CK_XARC81wHAAQLiAgMBGAI.zso?p=" + str(i) + "0&s=recentSalesStyle/desc/"
        url = "https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=goliveRecentSalesStyle/desc/&p=" + str(i)
        #https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=goliveRecentSalesStyle/desc/&p=1
        #https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=goliveRecentSalesStyle/desc/&p=2
        text = get_page(url)
        get_product_list(text)
    print(product_urls)
    start = 0
    stop = 2
    for i, url in enumerate(product_urls[start:stop]):
        product_page = get_page(url)
        parse_product_page(product_page,i)
    print('category: {}\n'.format(category))
    print('subcategory: {}\n'.format(subcategory))
    print('brand: {}\n'.format(brand))
    #print(img_urls)
    #batch_save_images()


def get_page(url):
    print(url)
    response = requests.get(url)
    return response.text

def get_product_list(text):
    BS = BeautifulSoup(text,'html.parser')
    #for product in BS.find("div",attrs={"class":"searchPage","id":"searchPage"}):
    outer = BS.find("div",attrs={"class":"searchPage"})
    #inner = outer.find("div")
    for i,product in enumerate(outer.find_all("article")):
        name_soup = product.find('p',attrs={'itemprop':'name'}) 
        name = name_soup.text
        print("NAME: {}".format(name))
        print('\n product #{}'.format(i))
        for t in product.text.split():
            print(t.strip() + '\n')
        url = product.find("a").attrs['href']
        print('\n product url' + '\n' + product.find("a").attrs['href'])
        product_urls.append("https://www.zappos.com" + url)
        split_url = url.split('/') 
        product_sku = split_url[4]
        product_color = split_url[6]
        print('SKU: {}\nColor: {}\n'.format(product_sku,product_color))
        skus_id.append(product_sku)
        colors_id.append(product_color)

#https://www.zappos.com/i/9045300/style/4318831/2
#<meta name="branch:deeplink:style" content="4478542" data-rdm="">



def parse_product_page(text,product_number):
    # get heirarchical data Shoes -> Sneakers & Athletic Shoes -> Brand
    soup = BeautifulSoup(text, 'html.parser') 
    header_data = soup.find('body',class_="activeMain").find('div',attrs={'id':'breadcrumbs'}).find_all('a')#('div',class_='SRGgm')
    #brand_data = soup.find('body',class_="activeMain").find('span',attrs={'itemprop':'brand'}).find('a')#('div',class_='SRGgm')
    ##name_data = soup.find('body',class_="activeMain").find('span',attrs={'itemprop':'name'}).find_all('a')#('div',class_='SRGgm')
    #print(brand_data)
    ##print(name_data)
    #brand = brand_data.text
    #print('brand: {}'.format(brand))
    ##name = name_data.text
    ##print('name: {}'.format(name))
    ##header_data = soup.find('body',class_="activeMain").find('div',id_='root').find_all('a')
    ##category.append(header_data[1].text)
    ##subcategory.append(header_data[2].text)
    ##brand.append(header_data[3].text)
    
    for i,head in enumerate(header_data):
        print('text #{}'.format(i) + head.text)
        if i==1:
            print('appending: {}'.format(head.text))
            category.append(head.text)
        elif i==2:
            print('appending: {}'.format(head.text))
            subcategory.append(head.text)
        elif i==3:
            print('appending: {}'.format(head.text))
            brand.append(head.text)

    head_soup = soup.find('head').find('meta',attrs={'name':'branch:deeplink:style'}) 
    print(head_soup)
    style_number = head_soup.attrs['content']
    styles_id.append(style_number)
    print('style_number: {}'.format(style_number))
    #title_soup = soup.find('head').find('meta',attrs={'property':'og:title'}) 
    #print(title_soup)
    #shoe_title = title_soup.attrs['content']
    #print(shoe_title)
#https://www.zappos.com/p/nunn-bush-nantucket-waterproof-plain-toe-oxford-black-wp/product/9093145/color/284531
    for i in [0,1,3,5,6]:
        #https://www.zappos.com/i/9045300/style/4318831/2
        img_site =  "https://www.zappos.com/i/" + skus_id[product_number] + "/style/" + styles_id[product_number] + '/{}'.format(i) 
        text = get_page(img_site)
        BS = BeautifulSoup(text,'html.parser')
        print(BS)
        img_soup = BS.find('img',attrs={'alt':'{}'.format(i)})
        img_url = img_soup.attr['src']
        print("IMG_URL: {}".format(img_url))


#https://m.media-amazon.com/images/I/71DSeJSkQQL._SX480_.jpg
#https://m.media-amazon.com/images/I/71DSeJSkQQL._SR106,78_.jpg


#https://www.zappos.com/p/nunn-bush-nantucket-waterproof-plain-toe-oxford-black-wp/product/9093145/color/284531
#https://www.zappos.com/p/nunn-bush-nantucket-waterproof-plain-toe-oxford-black-wp/product/9093145/color/284531
        #img_urls.append("http://www.zappos.com" + BS.find("a", id="angle-3").get("href"))
        #product_names.append(BS.title.string.split(' - ')[0].replace("/", "-"))

def save_img(url, i):
    resp = requests.get(url)
    fout = open(str(i) + "-" + str(product_names[i]) + ".jpg", "wb")
    fout.write(resp.content)
    fout.close()

def batch_save_images():
    threads = [gevent.spawn(save_img, img_urls[i], i) for i in range(len(img_urls))]
    gevent.joinall(threads)

main()

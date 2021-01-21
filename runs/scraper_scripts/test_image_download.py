import socks
import socket
import stem.process
import requests
from stem import Signal
from stem.control import Controller

def scrape_with_tor(url_request):
    SOCKS_PORT=9050# You can change the port number
    tor_process = stem.process.launch_tor_with_config(
        config = {
            'SocksPort': str(SOCKS_PORT),
        },
    )
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
                          addr="127.0.0.1",
                          port=SOCKS_PORT)
    socket.socket = socks.socksocket
    # ...

    with requests.urlopen(url_request) as response:
            try:
                page = response.read()
            except (http.client.IncompleteRead) as e:
                page = e.partial


            #response = requests.get(url_request)
            fout = open('image.jpg', "wb")
            fout.write(response.content)
            fout.close()
    # ...
    tor_process.kill()
def quick_test():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
    socket.socket = socks.socksocket
    print((requests.get('http://icanhazip.com')).content)
def new_scrape(url,i):
    torport = 9050
    proxies = {
        'http': "socks5h://localhost:{}".format(torport),
        'https': "socks5h://localhost:{}".format(torport)
    }
    print(requests.get('http://icanhazip.com', proxies=proxies).content)
    #fout = open('{}'.format(url), "wb")
    fout = open('image_{}.jpg'.format(i), "wb")
    response = requests.get(url, proxies=proxies)
    fout.write(response.content)
    fout.close()

def test_ip_with_tor():
    torport = 9050
    proxies = {
        'http': "socks5h://localhost:{}".format(torport),
        'https': "socks5h://localhost:{}".format(torport)
    }
    print(requests.get('http://icanhazip.com', proxies=proxies).content)
def test_ip_without_tor():
    print(requests.get("http://icanhazip.com").content)
# signal TOR for a new connection 
def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)
# Make a request through the Tor connection
# IP visible through Tor
test_ip_with_tor()
new_scrape("https://m.media-amazon.com/images/I/81w0lqDxyeL._SX480_.jpg",1)
# Above should print an IP different than your public IP

# Following prints your normal public IP
test_ip_without_tor()

# change IP
renew_connection()
# retest connection
test_ip_with_tor()
new_scrape("https://m.media-amazon.com/images/I/81w0lqDxyeL._SX480_.jpg",2)


#quick_test()
#scrape_with_tor("https://m.media-amazon.com/images/I/81w0lqDxyeL._SX480_.jpg")
#new_scrape("https://m.media-amazon.com/images/I/81w0lqDxyeL._SX480_.jpg")

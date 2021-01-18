import requests
from stem import Signal
from stem.control import Controller


def scrape(url):
    torport = 9050
    proxies = {
        'http': "socks5h://localhost:{}".format(torport),
        'https': "socks5h://localhost:{}".format(torport)
    }
    # print(requests.get('http://icanhazip.com', proxies=proxies).content)
    # fout = open('{}'.format(url), "wb")
    response = requests.get(url, proxies=proxies)
    return response.content


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
def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)


## Make a request through the Tor connection
## IP visible through Tor
test_ip_without_tor()
# test_ip_with_tor()
## Above should print an IP different than your public IP
#
## Following prints your normal public IP
# test_ip_without_tor()
#
## change IP
# renew_connection()
## retest connection
# test_ip_with_tor()
# new_scrape("https://m.media-amazon.com/images/I/81w0lqDxyeL._SX480_.jpg",2)
#
#
##quick_test()
##scrape_with_tor("https://m.media-amazon.com/images/I/81w0lqDxyeL._SX480_.jpg")
##new_scrape("https://m.media-amazon.com/images/I/81w0lqDxyeL._SX480_.jpg")

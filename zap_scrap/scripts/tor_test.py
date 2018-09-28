import requests
torport = 9050
proxies = {
    'http': "socks5h://localhost:{}".format(torport),
    'https': "socks5h://localhost:{}".format(torport)
}

print(requests.get('http://icanhazip.com', proxies=proxies).content)

from selenium import webdriver
profile=webdriver.FirefoxProfile()
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9050)
browser=webdriver.Firefox(profile)
browser.get("http://yahoo.com")
browser.save_screenshot("./screenshot.png")
browser.close()

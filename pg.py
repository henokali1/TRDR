from selenium import webdriver
from PIL import Image
from selenium.webdriver.chrome.options import Options
import time
import platform

url = 'https://www.binance.com/en/trade/BTC_BUSD'
fst = True

ptfrm = platform.platform()
if 'Linux' in ptfrm:
    driver = webdriver.Chrome(executable_path='chromedriver')
    dataset_dir = '/home/ubuntu/Documents/Projects/TRDR/raw-dataset/'
else:
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    dataset_dir = 'raw-dataset/'

#run first time to get scrollHeight
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)
# time.sleep(5)
# # Close Tut
# driver.find_elements_by_class_name("css-1wngn4j")[0].click()
# time.sleep(1)
# # Full Screen
# full_screen_btn = driver.find_elements_by_class_name("css-1gasmki")[0].click()

# time.sleep(1)
# driver.find_elements_by_class_name("css-rsvro8")[0].click()
# time.sleep(1)
# driver.find_elements_by_class_name("css-1ovzusp")[0].click()
time.sleep(30)
cntr = 0
# for i in range(10):
while 1:
    price = driver.title.split(' | ')[0].replace(',','')
    fn = dataset_dir + str(int(time.time())) + '-' + price + '-'
    driver.save_screenshot(f'{fn}.png')
    time.sleep(10)
    cntr += 1
    print(cntr, fn)
driver.close()

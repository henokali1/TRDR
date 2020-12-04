from selenium import webdriver
from PIL import Image
from selenium.webdriver.chrome.options import Options
import time
import platform

url = 'https://www.binance.com/en/trade/BTC_BUSD'
fst = True
#run first time to get scrollHeight
driver = webdriver.Chrome()
driver.get(url)
#pause 3 second to let page load
time.sleep(3)
#get scroll Height
height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
print(height)
#close browser
driver.close()

#Open another headless browser with height extracted above
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(f"--window-size=1920,{height}")
chrome_options.add_argument("--hide-scrollbars")
ptfrm = platform.platform()
if 'Linux' in ptfrm:
    driver = webdriver.Chrome(executable_path='chromedriver')
    dataset_dir = '/home/ubuntu/Documents/Projects/TRDR/raw-dataset/'
else:
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    dataset_dir = 'raw-dataset/'
driver = webdriver.Chrome(options=chrome_options)

cntr = 0
for i in range(5):
# while 1:
    driver.get(url)
    #pause 5 second to let page loads
    time.sleep(60)
    pl=driver.find_elements_by_class_name("css-8t380c")
    price = pl[0].text.split('\n')[0].replace(',','')
    # file name
    fn = dataset_dir + str(int(time.time())) + '-' + price + '-'
    # if fst:
    #     pass
    # else:
    #     fst = False
    #save screenshot
    driver.save_screenshot(f'{fn}.png')
    cntr += 1
    print(cntr, fn)
driver.close()
# 26.51
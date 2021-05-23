from selenium import webdriver
from PIL import Image
from selenium.webdriver.chrome.options import Options
import time

url = 'https://www.binance.com/en/trade/BTC_BUSD'

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
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver = webdriver.Chrome(options=chrome_options)

for i in range(4):
    driver.get(url)
    #pause 5 second to let page loads
    time.sleep(5)

    # file name
    fn = str(int(time.time()))
    #save screenshot
    driver.save_screenshot(f'screenshot/{fn}.png')
driver.close()

"""
This function determines if the chromedriver version is up to date

From here it is up to the script writter how to handle the error
"""


"""
Version 1: 
Import of selenium outside of package.  This would be for when Selenium is already running  in the script
"""
## Import packages
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver: WebDriver = webdriver.Chrome(options=options,executable_path='//tpdcipdiv01-efdv.hca.corpad.net/EFDV/Dept/EDFL/SIG/ACFO Reports/2. VISTA Comps/ChromeDriver/chromedriver.exe')

##fucntion
def drivercheck():
    browserVer = driver.capabilities['browserVersion']
    driverVer = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    if browserVer[:-3]==driverVer[:-3]:
        print('Driver Good!')
    else:
        print('Download new driver')

drivercheck()

"""
Version 2:
Import of selenium inside of package, this is to check before running the script
"""

path='//path/ChromeDriver/chromedriver.exe'

## Import packages


##fucntion
def drivercheckimport(path):
    from selenium import webdriver
    from selenium.webdriver.chrome.webdriver import WebDriver

    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver: WebDriver = webdriver.Chrome(options=options,executable_path=path)
    browserVer = driver.capabilities['browserVersion']
    driverVer = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    if browserVer[:-3]==driverVer[:-3]:
        print('Driver Good!')
    else:
        print('Download new driver')

drivercheckimport(path)


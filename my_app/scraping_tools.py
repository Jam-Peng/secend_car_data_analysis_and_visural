#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 02:01:04 2023

@author: pengjam
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os, time


chrome_driver=f"r'{os.getcwd()}/webdriver/chromedriver'"

# Get chrome
def get_chrome(url, driver_path=chrome_driver, hide=False, wait=10):
    try:
        options=webdriver.ChromeOptions()
        if hide:
            options.add_argument('--headless')
        
        service=Service(driver_path)
        chrome=webdriver.Chrome(service=service, options=options)
        chrome.implicitly_wait(wait)
        chrome.get(url)
        return chrome
    except Exception as e:
        print(e)
    return None


# Get element
def get_element(chrome, xpath):
    try:
        return chrome.find_element(By.XPATH, xpath)
    except Exception as e:
        print(e)
    return None


if __name__ == '__main__':
    url = 'https://tw.yahoo.com/'
    chrome = get_chrome(url)
    time.sleep(5)
    chrome.quit()
    
    
#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-16,14:56"

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
poll = ThreadPoolExecutor(50)

def get_goods(driver):
    for i in range(24):
        goods = driver.find_elements_by_id("result_{0}".format(i))
        for good in goods:
            good_image = good.find_element_by_css_selector(".cfMarker").get_attribute("src")
            good_url = good.find_element_by_css_selector(".a-link-normal").get_attribute("href")
            good_name = good.find_element_by_css_selector(".s-color-twister-title-link h2").text
            good_price = good.find_element_by_css_selector(".a-color-price").text

            msg = "商品图片：%s,链接：%s,商品名：%s,商品价格：%s"%(good_image,good_url,good_name,good_price)
            print(msg,end = "\n\n")

    button = driver.find_element_by_css_selector(".pagnRA a")
    button.send_keys(Keys.DOWN)
    get_goods (driver)


def spider(url,keyword):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(5)

    try:
        input_tag = driver.find_element_by_id("twotabsearchtextbox")
        input_tag.send_keys(keyword)
        input_tag.send_keys(Keys.ENTER)

        time.sleep(1)
        get_goods(driver)
    except Exception:
        pass
    finally:
        driver.close()


if __name__ == '__main__':
    poll.submit(spider,"https://www.amazon.cn/","iphone")
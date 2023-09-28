#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
import os,shutil

# 测试用例判断是否正确的验证方法
class Browserdef:

    def __init__(self):
        #判断是否有googledata文件夹,有则递归删除
        if os.path.exists("googledata"):
            shutil.rmtree( "googledata" )
        else:
            pass


        # 使用chromedriver 
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        #文件夹,用来存储google数据。
        self.options.add_argument("user-data-dir=./googledata")
        self.options.add_argument('--headless') # 不显示界面模式
        
        self.browser = webdriver.Chrome(options=self.options)
        

        self.getBy = By
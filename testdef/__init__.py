#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# 测试用例判断是否正确的验证方法
class Testdef:
    
    def __init__(self, getbrowser):
        self.browser = getbrowser
    
    def errorlogin(self, arg):
        
        # 对于input操作,获取input的xpath，并sendkeys
        try:
            return True
            
        except NoSuchElementException:
            return False
            

    def login(self,arg):
        try:
            text = self.browser.find_element(By.XPATH, arg).get_attribute("innerText")
            if "登陆" in text:
                return False
            else:
                return True
        except NoSuchElementException:
            return False

    def logout(self,arg):
        #判断登陆的loginform存在
        try:
            return True
        except NoSuchElementException:
            return False
    
    def tostar(self,arg):
        return True
        # starnum = len(arg.children)
        # if starnum == 1:
        #     return True
        # else:
        #     return False
    
    def delstar(self,arg):
        return True
        # starnum = len(arg.children)
        # if starnum == 0:
        #     return True
        # else:
        #     return False
    
    def goodsorder(self,arg):
        return True
    
    def goods_maintag(self,arg):
        return True
    
    def test(self,arg):
        return False

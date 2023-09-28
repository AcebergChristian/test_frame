#!/usr/bin/env python
import sys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from json.decoder import JSONDecodeError
from browserdef import Browserdef
from parsexcel import ParseExcel
from testdef import Testdef
from sqldef import Sqldef
from toreport import Toport
import time
import os,shutil
import json


# 大循环每一个case，判断结果成功与否，计入数据库
class Executedef(Browserdef):
    
    def __init__(self):
        super().__init__()
        
        #实例化 测试方法模块,并传值(selenium的操作浏览器的方法)进去
        self.testdef = Testdef(self.browser)
        #实例化 连接插入数据库模块,用于存储测试用例执行结果
        self.sqldef = Sqldef()

    def get_exceldata(self):
        # 使用ParseExcel类
        exceldata = ParseExcel()
        #返回ParseExcel get_arrdata方法的数据(平铺)
        #print(exceldata.get_arrdata())
        return exceldata.get_arrdata()
    
    def loopoperate(self):
        operateprocess = Operateprocess(self.browser)
        
        
        for item in self.get_exceldata():
            print("*********正在执行第{}个sheet的第{}个测试用例*********".format(item["sheet"],item["no"]))
            
            #获取开始执行此条用例的时间
            t1 = time.time()
            starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            try:
                kdt_stepjson = json.loads(item["kdt_step"], strict=False)
                for jtem in kdt_stepjson:
                    print("正在{},方法为{}".format(jtem["stepname"],jtem["operate"]))
                    operateprocess( jtem )
            
                #获取此条用例执行结束的时间
                t2 = time.time()
                #获取此条用例的运行时间
                run_time = round( (t2 - t1),2 )
                print(f"此条测试用例运行时间为 {run_time}s")
                
                #用testdef方法判断此条测试用例通过没有
                if getattr(self.testdef, item["veritydef"])( item["veritypath"] ):
                    self.sqldef.insertsql(item["no"], item["mod"], item["title"], item["details"], item["operate_step"], item["kdt_step"].replace("'", "\\'"), item["veritydef"], item["veritypath"], item["priority"], item["responsibler"], item["remarks"], starttime, run_time, True)
                    
                else:
                    # 当执行验证发生错误时, 记录错误信息到mysql的TEST_RES表
                    self.sqldef.insertsql(item["no"], item["mod"], item["title"], item["details"], item["operate_step"], item["kdt_step"].replace("'", "\\'"), item["veritydef"], item["veritypath"], item["priority"], item["responsibler"], item["remarks"], starttime, run_time, False)
                    # 当执行验证发生错误时, 截图
                    self.browser.get_screenshot_as_file("testerror_pic/error_{}.png".format(time.strftime("%Y_%m_%d %H_%M_%S")))
            
            except JSONDecodeError:        
                #打印文字,此条用例已经测试结束
                print("*********第{}个测试用例执行完毕*********\n".format(item["no"]))
                
                #执行完一个case后 等待3s
                self.browser.implicitly_wait(3)
            


        #打印文字,请等待
        print("所有测试用例已经执行完毕,请等待...")
        time.sleep(3)
        #实例化 生成报告的类,并传入sqldef查到的数据
        self.toport = Toport( self.sqldef.getdata() )
        #打印文字,正在生成报告
        time.sleep(3)
        print("正在生成报告...")
        self.toport.tojinja2()
        #随便拿一个数据【alltime】判断，如果有则生成报告成功
        if self.toport.getdata["alltime"]:
            print("报告已经生成,3秒后关闭...")
            time.sleep(3)
            self.browser.quit()
        else:
            print("报告生成出错,请检查...")
            


# 封装数组每个json来 所执行的步骤
class Operateprocess:
    
    def __init__(self, getbrowser):
        self.browser = getbrowser

    def  __call__(self, data):
 
        if data["operate"] == "openlink":
            # 对于openlink操作,打开对应url
            self.browser.get(data["url"])
            self.browser.implicitly_wait(2)
            #self.browser.quit()
            
        elif data["operate"] == "input":
            # 对于input操作,获取input的xpath，并sendkeys
            try:
                self.browser.find_element(By.XPATH, data["ele_path"]).send_keys( data["value"] )
                self.browser.implicitly_wait(2)
                
            except NoSuchElementException:
                pass
  
            
        elif data["operate"] == "click":
            # 对于click操作,点击该元素
            try:
                self.browser.find_element(By.XPATH, data["ele_path"]).click()
                self.browser.implicitly_wait(3)
                
            except NoSuchElementException:
                pass
        
        elif data["operate"] == "switchtab":
            tablist = self.browser.window_handles
            
            self.browser.switch_to.window(tablist[data["value"]])
            


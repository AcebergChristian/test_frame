#!/usr/bin/env python
import pymysql
from jinja2 import Environment, FileSystemLoader
import time


# 测试用例判断是否正确
class Toport:
    
    def __init__(self, arg):
        self.getdata = arg

    def tojinja2(self):

        restime = time.strftime("%Y-%m-%d %H%M%S", time.localtime())
        
        # 加载Jinja2模板
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('report_mode/template.html')

        # 使用Jinja2填充模板
        report_content = template.render(data=self.getdata)

        # 将填充后的内容写入HTML文件
        with open('test_report/report_{}.html'.format(restime), 'w') as f:
            f.write(report_content)
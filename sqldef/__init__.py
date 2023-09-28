#!/usr/bin/env python
# 打开数据库连接
import pymysql


# 测试用例判断是否正确
class Sqldef:
    
    def __init__(self):
        self.connect_create_table()
        self.del_data()
        
    def connect_create_table(self):
        self.db = pymysql.connect(host="localhost",
                     user="root",
                     password="12345678",
                     database="mysql",
                     use_unicode=True,
                     charset='utf8')
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()        
        
    def del_data(self):

        # 使用预处理语句创建表
        sql = ''' delete from TEST_RES  '''
    
        # 执行sql语句
        self.cursor.execute(sql)
        # 提交sql语句
        self.db.commit()
        # 关闭数据库连接
        self.db.close()
    
    def insertsql(self, no, modname, title, details, operate_step, kdt_step, veritydef, veritypath, priority, responsibler, remarks, starttime, run_time, run_res):
        
        #每次执行插入操作时先连接
        self.connect_create_table()
        
        # SQL 插入语句
        sql = "INSERT INTO TEST_RES(no, \
            modname, title, details, operate_step, kdt_step, veritydef, veritypath, priority, responsibler, remarks ,starttime, run_time, run_res) \
            VALUES ('%s', '%s',  '%s',  '%s', '%s' ,'%s' ,'%s' ,'%s' ,'%s' ,'%s' ,'%s' ,'%s' ,%f ,%s )" % \
            (no, modname, title, details, operate_step, kdt_step, veritydef, veritypath, priority, responsibler, remarks, starttime, run_time, run_res)
        
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交sql语句
            self.db.commit()
            # 关闭游标连接
            self.cursor.close()
            # 关闭数据库连接
            self.db.close()
            
        except:
            # 发生错误时回滚
            self.db.rollback()
            #关闭数据库连接
            self.db.close()
            
    def getdata(self):
        
        # 获取所有数据个数
        allnum = self.getdatasql("select count(*) from TEST_RES")[0][0]
        
        # 获取成功数据个数
        success_num = self.getdatasql("select count(*) from TEST_RES where run_res = 1")[0][0]
        
        # 获取失败数据个数
        fail_num = self.getdatasql("select count(*) from TEST_RES where run_res = 0")[0][0]
        
        # 获取所有字段
        allfiled = []
        for item in self.getdatasql("describe TEST_RES"):
            allfiled.append(item[0])
            
        # 获取所有时间总和
        alltime = self.getdatasql("SELECT CAST(SUM(run_time) AS FLOAT) FROM TEST_RES;")[0][0]
        
        # 获取所有数据
        alldata = []
        
        for item in self.getdatasql("select * from TEST_RES"):
            itemjson = {}
            for jndex , jtem in enumerate(item):
                # if allfiled[jndex] == "starttime":
                #     itemjson[ allfiled[jndex] ] = jtem.strftime("%Y-%m-%d %H:%M:%S")
                # elif allfiled[jndex] == "run_time":
                #     itemjson[ allfiled[jndex] ] = float(jtem)
                # else:
                itemjson[ allfiled[jndex] ] = str(jtem)
                    
            alldata.append(itemjson)
        # 获取modname 的所有类型
        modtype = []
        for item in self.getdatasql("select t.modn as modname from (select distinct(modname) as modn from TEST_RES) t"):
            modtype.append(item[0] )
        res = {
            "allnum": allnum,
            "success_num": success_num,
            "fail_num": fail_num,
            "alldata": alldata,
            "modtype": modtype,
            "alltime":alltime,
            "allfiled":[ 'no','modname','title', 'details','operate_step','kdt_step',  'veritydef', 'veritypath',  'priority',  'responsibler','remarks',  'starttime', 'run_time','run_res']
            }
        
        #print(res)
        return res
    

    # 获取数据总数sql
    def getdatasql(self , sqltext):
        self.db = pymysql.connect(host="localhost",
                     user="root",
                     password="12345678",
                     database="mysql",
                     use_unicode=True,
                     charset='utf8')
 
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()        
        
        # SQL 插入语句
        sql = sqltext
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交执行
            self.db.commit()
            # 获取数据
            data = self.cursor.fetchall()
            # 关闭游标连接
            self.cursor.close()
            # 关闭数据库连接
            self.db.close()
            
            return data
            
        except:
            # 发生错误时回滚
            self.db.rollback()
            # 关闭数据库连接
            self.db.close()
            
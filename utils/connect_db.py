#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from utils.dateencoder_json import DateEncoder
import pymysql
import json


class Operate_Mysql():
    def __init__(self,host='rm-wz9wv0ifw04w75r514o.mysql.rds.aliyuncs.com',port=3306,user='star_test',password='ymFAX!54wzUW',database='bladex_test',charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset


    #初始化数据库,游标
    def open(self):

        #连接数据库
        self.conn = pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,database=self.database,charset=self.charset)
        self.cur = self.conn.cursor()


    #关闭游标,关闭数据库
    def colse(self):
        self.cur.close()
        self.conn.close()


    #增删改操作
    def sql_execute(self,sql,L=[]):
        self.open()
        try:
            self.cur.execute(sql,L)  # 执行sql命令
            self.conn.commit()  # 提交到数据库执行
            print('OK,SQL命令执行成功')
            return 'OK,SQL命令执行成功'
        except Exception as err:
            self.conn.rollback()
            print('failed,SQL命令执行失败', err)
            return 'failed,SQL命令执行失败'
        self.colse()


    #查询操作
    def sql_query(self, sql,L=[]):
        self.open()
        self.cur.execute(sql,L)
        result = self.cur.fetchall()
        result = json.dumps(result,cls=DateEncoder,ensure_ascii=False)
        self.colse()
        return json.loads(result)







if __name__ == '__main__':
    op_mysql = Operate_Mysql()
    res = op_mysql.sql_query("select * from uas_car_brand ")
    print(res)




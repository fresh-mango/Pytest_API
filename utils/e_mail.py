#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import smtplib
from utils.operate_config import ParserConfig,report_path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class E_mail():

    def __init__(self):
        self.parser = ParserConfig()
        self.email_host =self.parser.get_section_options(node = 'email',key='email_host')
        self.send_user =self.parser.get_section_options(node = 'email',key='send_user')
        self.password =self.parser.get_section_options(node = 'email',key='authoriz')
        self.receivers =self.parser.get_section_options(node = 'email',key='receivers')

    def get_attach_file(self):
        # 列举参数：report_path目录下的所有文件（名），结果以列表形式返回。
        # lists = os.listdir(report_path)
        # # 对lists元素，按文件修改时间从小到大排序。
        # lists.sort(key=lambda fn: os.path.getatime(report_path + "\\" + fn))
        # file_new = os.path.join(report_path, lists[-1])
        file_new = os.path.join(report_path + "\\" + 'index.html')


        return file_new


    def message_config(self, att_file=None):
        message = MIMEMultipart()
        message.attach(MIMEText('这是自动化测试报告，请查阅',_subtype='plain',_charset='utf-8'))
        message['Subject'] = '自动化测试报告'
        message['From'] = self.send_user
        message['To'] = self.receivers

        # 通过MIMEApplication构造附件
        file_name = os.path.basename(self.get_attach_file())
        att = MIMEApplication(open(self.get_attach_file(), 'rb').read())
        att["Content-Type"] = 'application/octet-stream'
        att.add_header('content-disposition', 'attachment', filename=file_name)
        message.attach(att)

        server = smtplib.SMTP()
        server.connect(self.email_host)
        server.login(self.send_user, self.password)
        server.sendmail(self.send_user, self.receivers.split(';'), message.as_string())
        server.close()

        return message



    def send_email(self):
        flag = self.parser.get_section_options(node='email', key='on_off')
        if flag == 'on':
            self.message_config()
        else:print("邮件发送失败，请检查邮件配置是否正确！")

if __name__ == '__main__':


    e = E_mail()
    e.send_email()

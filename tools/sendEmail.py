#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/3 12:41
# @Author  : Glory Gu
import os
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from tools.tool import retry


# @retry(3, "send email")
# def send_email(mail_title, mail_body, files, path, test, smtp_server, sender, username, password, receiver_list,
#                cc_list, receiver_list_test):
#     # 邮件内容, 格式, 编码
#     message = MIMEMultipart()
#     message.attach(MIMEText(mail_body, 'html', 'utf-8'))
#     message['From'] = sender
#     _receivers = receiver_list_test if test else receiver_list
#     # _cc_receivers = receiver_list_test if test else cc_list
#     _cc_receivers = cc_list
#     message['To'] = ', '.join(_receivers)
#     message['Cc'] = ', '.join(_cc_receivers)
#     message['Subject'] = Header(mail_title, 'utf-8')
#
#     for file in files:
#         file_path = os.path.join(path, file)
#         if os.path.isfile(file_path):
#             # 构造附件
#             with open(file_path, 'rb') as _f:
#                 _text = _f.read()
#                 att = MIMEBase('application', "octet-stream")
#                 att.set_payload(_text)
#                 att["Content-Type"] = 'application/octet-stream'
#                 # att.add_header("Content-Disposition", "attachment", filename=("utf-8", "", file))  # 不兼容outlook
#                 # 兼容outlook，名称显示为 未命名的附件.dat问题
#                 att.add_header("Content-Disposition", "attachment", filename=Header(file, "utf-8").encode())
#                 encoders.encode_base64(att)
#                 message.attach(att)
#
#     print('sending email: \n\tTo: %s\n\tCc: %s' % (_receivers, _cc_receivers))
#     with smtplib.SMTP_SSL(smtp_server) as smtp:
#         smtp.login(username, password)
#         smtp.sendmail(sender, _receivers + _cc_receivers, message.as_string())
#         print("send email successfully !")


# if __name__ == '__main__':
#     from config.globals.emailinfo import data
#
#     with open('../report/report.html', mode='r', encoding='utf-8') as f:
#         _mail_body = f.read()
#     # _files = ['3.13提测需求统计.xlsx', 'bug统计(2020-03-09 至 2020-03-28).xlsx']
#     #  _path = 'D:\development\hand\gen_report\\report\\20200405211849'
#
#     _files = ['report.html']
#     _path = ""
#     send_email('自动化测试报告', "", _files, '../report', True, **data['email'])

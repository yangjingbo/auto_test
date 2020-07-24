# -*- coding:utf-8 -*-
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shutil
import zipfile
import datetime
from moats import GlobalVar
import configparser



def project_root_path(filename):
    """得到加路径的文件名
    filename:从根路径出发的文件名
    """
    obj_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    obj_path = str(obj_path)
    obj_path = obj_path.replace('\\', '/')
    obj_path = (obj_path + '/' + filename)
    return obj_path


def clear_report(dirname):
    """清空日志和截图的文件夹"""
    try:
        shutil.rmtree(dirname)
    except BaseException:
        print(BaseException)


def screenshot_for_report(driver):
    """
    实现报告截图
    :param driver: 实例化的webdriver
    :return: None
    """
    env = GlobalVar.ENVIRONMENT
    nowtime = datetime.datetime.now()
    png_name = nowtime.strftime("%Y%m%d%H%M%S") + '.png'
    file_path = os.path.join(env['report_dir'], png_name)
    driver.get_screenshot_as_file(file_path)
    print('screenshot:', png_name)


def mkdir(path):
    """
    创建目录
    :param path: 将要创建的目录路径
    :return: True or False
    """
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False


def make_zip(source_dir, output_filename):
    """
    将文件打包
    :param source_dir: 要打包的资源目录
    :param output_filename: 打包后的zip包路径
    :return: None
    """
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


def make_mail_content(result, start_time, duration_time):
    """
    拼接邮件正文内容
    :param result: 测试结果
    :param start_time: 测试开始时间
    :param duration_time: 测试结束时间
    :return: 邮件正文内容
    """
    r = str(result)
    r = r.replace('<', '=')
    r = r.replace('>', '=')
    r = r.replace('.', '=')
    r = r.replace(' ', '=')
    middle = r.split('=')
    success = int(middle[5]) - int(middle[7]) - int(middle[9])
    content = '测试时间：' + str(start_time)[0:19] + '<br />' + '测试执行消耗：' + str(duration_time) + '<br />' + '全部用例：' + middle[
        5] + '个<br />' + '通过：' + str(success) + '个<br />' + '失败：' + middle[9] + '个<br />' + '执行错误：' + middle[7] + '个'
    if middle[7] == '0' and middle[9] == '0':
        content = '<html><body bgcolor="rgb(0,255,0)"><h1>测试项目：骑士团</h1><h2 style="color:green">' + content + '</h2><h3>用例详情见附件</h3></html>'
    else:
        content = '<html><body bgcolor="rgb(255,0,0)"><h1>测试项目：骑士团</h1><h2 style="color:red">' + content + '</h2><h3>用例详情见附件</h3></html>'
    return content


def send_mail(result, start_time, duration_time):
    """
    发送邮件
    :param result: 测试结果
    :param start_time: 测试开始时间
    :param duration_time: 测试结束时间
    :return: 无
    """
    env = GlobalVar.ENVIRONMENT
    subject = str(env['subject']) + '_' + str(datetime.datetime.now())[:10]
    smtpserver = env['smtp_server']
    user = env['smtp_user']
    password = env['smtp_password']
    sender = env['smtp_user']
    receivers = env['receivers'].split(',')
    content = make_mail_content(result, start_time, duration_time)
    with open(env['report_zip_name'], 'rb')as file:
        send_file = file.read()
    att = MIMEText(send_file, 'base64', 'utf-8')
    att['Content-Type'] = 'application/octet-stream'
    att['Content-Disposition'] = 'attachment;filename="recently_report.zip"'

    msgroot = MIMEMultipart()
    msgroot.attach(MIMEText(content, 'html', 'utf-8'))
    msgroot['Subject'] = subject
    msgroot['From'] = sender
    msgroot['To'] = ','.join(receivers)
    msgroot.attach(att)

    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    smtp.helo(smtpserver)
    smtp.ehlo(smtpserver)
    smtp.login(user, password)

    print('Start send email......')
    smtp.sendmail(sender, receivers, msgroot.as_string())
    smtp.quit()
    print('Send email end!')

    """读取CSV文件里的某个单元格数据
        file_name: 要读取的CSV文件，包含路径
        row_num"要读取的单元格的行号
        col_num:要读取的单元格的列号
    """


def get_value_with_key(test_class, key):
    """
    :param test_class:
    :param key:
    :param filename:
    :return:
    """
    env = GlobalVar.ENVIRONMENT
    filename = env['test_data_file']
    cf = configparser.ConfigParser()
    cf.read(filename, encoding='utf-8')
    value = cf.get(test_class, key)
    return value



def get_list_with_key(test_class, key):
    """
    :param test_class:
    :param key:
    :param filename:
    :return:
    """
    env = GlobalVar.ENVIRONMENT
    filename = env['test_data_file']
    cf = configparser.ConfigParser()
    cf.read(filename, encoding='utf-8')
    values = cf.get(test_class, key).replace('[', '').split(']')
    values.remove('')
    return values


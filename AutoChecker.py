#!/usr/bin/env python
# coding: utf-8


import requests
import re
import time
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt 
from bs4 import BeautifulSoup
# 请求头信息

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language': 'en',
    'Cache-Control': 'max-age=0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT':'1',
    'Host':'sep.ucas.ac.cn',
    'Origin': 'http://sep.ucas.ac.cn',
    'Referer': 'http://sep.ucas.ac.cn/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

regex = re.compile(r"'(.*?)'")

sep_link = "http://sep.ucas.ac.cn/slogin"

params_nocode = {'userName':'Your user name', # 填入用户名
          'pwd':'your password', #填入密码
          'sb':'sb'}
params_withcode = {'userName':'Your user name',#填入用户名
          'pwd':'your password', #填入密码
          'certCode': '',
          'sb':'sb'}


def localtime():
    return time.asctime( time.localtime(time.time()) )



import logging
from logging import handlers

screen_log = True

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(th)
        
        if (screen_log == True): # log 输出到屏幕
            sh = logging.StreamHandler()#往屏幕上输出
            sh.setFormatter(format_str) #设置屏幕上显示的格式
            self.logger.addHandler(sh) #把对象加到logger里


# global logger
log = Logger('Log.log',level='debug')

# if __name__ == '__main__':
#     log = Logger('test.log',level='debug')
#     log.logger.debug('debug')
#     log.logger.info('info')
#     log.logger.warning('警告')
#     log.logger.error('报错')
#     log.logger.critical('严重')
#     Logger('error.log', level='error').logger.error('error')



import smtplib
#发送字符串的邮件
from email.mime.text import MIMEText
#处理多种形态的邮件主体我们需要 MIMEMultipart 类
from email.mime.multipart import MIMEMultipart
#处理图片需要 MIMEImage 类
from email.mime.image import MIMEImage
 
#设置服务器所需信息
fromaddr = ' your@email.address'#邮件发送方邮箱地址
password = 'your password' #密码(部分邮箱为授权码) 

toaddrs = ['receive@email.address1','receive@email.address2']#邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
 
def SendEmail(Id, Time):
    #设置email信息
    #---------------------------发送字符串的邮件-----------------------------
    #邮件内容设置
    message = MIMEText('人文讲座'+ Id + '已报名, 讲座时间为' + Time ,'plain','utf-8')
    #邮件主题       
    message['Subject'] = '人文讲座' + Id +'报名成功!'
    #发送方信息
    #message['From'] = 'Saplace' 
    #接受方信息     
    #message['To'] = 'You'
    #---------------------------------------------------------------------


    #登录并发送邮件
    try:
        server = smtplib.SMTP('smtp.office365.com',587) #
        server.ehlo()
        server.starttls()
        server.login(fromaddr,password)
        server.sendmail(fromaddr, toaddrs, message.as_string())
        log.logger.info('Email Success')
        server.quit()
        return True
    except smtplib.SMTPException as e:
        log.logger.error(e) #打印错误
        return False



s = requests.Session()
c = requests.Session()
HLcheck = dict()
while True:
    
    humanityLecture = c.get(url = 'http://jwxk.ucas.ac.cn/subject/humanityLecture')
    hl = BeautifulSoup(humanityLecture.text, 'lxml')
    if (hl.find(string="你的会话已失效或身份已改变，请重新登录") != None):
        try:
            # -------------------  login jwxk ------------------------ 
            jwxk = s.get('http://sep.ucas.ac.cn/portal/site/226/821')
            jwxk = BeautifulSoup(jwxk.text, 'lxml')
            j_link = jwxk.noscript.meta.attrs['content'][6:]

            c = requests.Session()
            j_login = c.get(url=j_link,cookies = s.cookies.get_dict())
            requests.utils.add_dict_to_cookiejar(c.cookies, {'sepuser': s.cookies.get_dict()['sepuser']}) # set jwxk cookies
            # -------------------------------------------------------
        except Exception as e:
            log.logger.error('jwxk Login Error %s'%e)
            
            try:
                    # ------------------- login sep -------------------------
                    s = requests.Session()
                    Sep_Login = s.post(url=sep_link, data=params_nocode,headers=headers,verify=False,timeout=10) # login
                    sl = BeautifulSoup(Sep_Login.text, 'lxml')

                    if (sl.find('input', attrs={'name':'certCode'}) !=None):  # verCode needed
                        vpic = s.get('http://sep.ucas.ac.cn/changePic?code='+str(int(round(time.time() * 1000))))
                        image = Image.open(BytesIO(vpic.content))
                        image.show()
                        plt.imshow(image)
                        plt.show()
                        
                        #SendEmail(' 需要登录验证码 ','000')
                        vcode = input()
                        
                        
                        params_withcode['certCode'] = vcode
                        Sep_Login = s.post(url=sep_link, data=params_withcode,headers=headers,verify=False,timeout=10) 
                        sl = BeautifulSoup(Sep_Login.text, 'lxml')

                    if (sl.find('a',title='退出系统') == None): # check login status
                        raise Exception("Sep Login Error")
                    # -------------------------------------------------------
            except Exception as e:
                log.logger.error(e)
            else:
                log.logger.info('Sep login at %s'%localtime())
        else:
                log.logger.info('jwxk login at %s'%localtime())
    else:
        for alec in hl.find_all("a",string='报名'):
            plist = regex.findall(alec.attrs['onclick'])
            pdict = {'lectureId': plist[0],
                     'communicationAddress': plist[1]}
            res = c.post(url='http://jwxk.ucas.ac.cn/subject/toSign',data = pdict)
            
            if (res.text == 'success'): # Send an Email 
                if (plist[0] not in HLcheck):
                    if (SendEmail(plist[0],plist[1])):
                        HLcheck[plist[0]] = 1 

            log.logger.info('%s %s %s'% (localtime(),str(pdict),res.text) )
                
        log.logger.info('Check at %s'% (localtime()) )
        time.sleep(5)



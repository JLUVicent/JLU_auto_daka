import time
from selenium import webdriver
# from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from selenium.webdriver.common.keys import Keys


# 发送邮箱任务


def email(receivers, content):
    # 设置服务器所需信息
    # 163邮箱服务器地址
    mail_host = 'smtp.163.com'
    # 你的163用户名
    mail_user = ''
    # 你的邮箱授权码
    mail_pass = ''
    # 邮件发送方邮箱地址（设置发送方邮箱）
    sender = ''
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [receivers]

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = 'JLUVicent打卡小助手汇报'
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]

    # 登录并发送邮件
    try:
        # 启动
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        # 连接到服务器
        smtpObj.connect(mail_host, 465)
        # smtpObj = smtplib.SMTP(mail_host, 25, timeout=300)

        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误


def driver():
    # 创建浏览器对象
    # path = 'chromedriver.exe'
    # 隐式浏览器
    path = 'phantomjs.exe'
    # browser = webdriver.Chrome(path)

    browser = webdriver.PhantomJS(path)

    # 研究生打卡入口
    url = 'https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start'
    # 本科生打卡入口
    # url = 'https://ehall.jlu.edu.cn/infoplus/form/BKSMRDK/start'

    browser.get(url)
    return browser


def log_in(browser, username, password):
    input = browser.find_element_by_id('username')
    input.send_keys(username)
    pwd_input = browser.find_element_by_id('password')
    pwd_input.send_keys(password)
    log_in = browser.find_element_by_id('login-submit')
    log_in.click()


def submmit(browser):
    sub_button = browser.find_element_by_link_text(
        '提交')

    sub_button.click()
    time.sleep(3)
    ensure_button = browser.find_element_by_xpath(
        '//button[@class="dialog_button default fr"]')
    ensure_button.click()
    time.sleep(3)
    ok_botton = browser.find_element_by_xpath(
        '//button[@class="dialog_button default fr"]')
    ok_botton.click()


# 程序入口
if __name__ == '__main__':
    # 打卡登录账号
    username_list = []
    # 称呼
    name_list = ['王先森']
    # 打卡登录密码
    password_list = []
    # 打卡完成后信息接收方邮件，注意这几个都是字符串str形式存储的，例如'王先森'这样的。
    receivers_list = []

    # 这块的flag是一个纠错标志位，表示第一次打卡不成功的话重新尝试一次，一共尝试三次如果还不成功，则说明密码有问题。
    # flag表示是否跳出循环标志位
    flag = 1
    # number表示尝试次数
    number = 0
    for i in range(len(username_list)):
        # if i == 0:
        while True:
            try:
                browser = driver()
                time.sleep(3)
                username = username_list[i]
                password = password_list[i]
                log_in(browser, username, password)
                time.sleep(10)
                submmit(browser)
                # 隐式浏览器快照
                # browser.save_screenshot(username_list[i]+'.png')
                time.sleep(3)
                # 退出
                browser.quit()

                # number = number_list[i]
                # 发送短信
                # body = f'{username}打卡完成'
                # send_sms(number=number, body=body)

                content = f'{name_list[i]}打卡成功'
                email(receivers_list[i], content)
                print(f'{name_list[i]}打卡完成')
                flag = 0
            except:
                flag = 1
                number += 1
                if number == 3:
                    dcontent = f'{name_list[i]}打卡失败，请联系管理员JLUVicent修改密码'
                    print(f'{name_list[i]}打卡失败')
                    email(receivers_list[i], dcontent)
            if flag == 0 or number == 3:
                break

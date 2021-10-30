import time
from selenium import webdriver
# from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from selenium.webdriver.common.keys import Keys


# 发送邮箱任务
# 和研究生打卡程序一样

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
    path = r'C:\Users\Administrator\Desktop\jlu_daka\jlu_daka\chromedriver.exe'
    # 隐式浏览器
    # path = 'phantomjs.exe'
    browser = webdriver.Chrome(path)

    # browser = webdriver.PhantomJS(path)

    # 研究生url
    # url = 'https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start'
    # 本科生url
    url = 'https://ehall.jlu.edu.cn/infoplus/form/BKSMRDK/start'

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

# 和研究生打卡不一样的地方，多了一个复选框


def dangshi(browser):
    time.sleep(5)
    windows = browser.window_handles
    user1 = browser.find_element_by_xpath(
        "/html/body/div[4]/form/div/div[3]/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[4]/td/font/div/div/iframe")
    for i in range(60):
        user1.send_keys(Keys.DOWN)  # 滑动
    time.sleep(5)
    browser.execute_script('window.scrollBy(0,250)')  # 竖向滚动条操作
    time.sleep(5)
    # browser.find_element_by_xpath(
    #     '/html/body/div[4]/form/div/div[3]/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[13]/td[3]/div/div/label[1]/font').click()
    time.sleep(3)
    iframe = browser.find_element_by_xpath(
        '/html/body/div[4]/form/div/div[3]/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[4]/td/font/div/div/iframe')

    browser.switch_to.frame(iframe)
    target = browser.find_element_by_xpath('//*[@id="wty"]')
    time.sleep(1)
    browser.execute_script("arguments[0].click();", target)
    browser.switch_to.default_content()


def temp(browser):
    wendu = browser.find_element_by_xpath(
        '//div//label[@for="V1_CTRL28"]')
    wendu.click()


# 程序入口
if __name__ == '__main__':
    # 打卡系统登录名注意全部为str形式
    username_list = []
    # 邮件称呼名，随便啥都行
    name_list = []
    # 用户登录密码
    password_list = []
    # 接受信息方邮箱
    receivers_list = []
    # flag表示是否跳出循环标志位
    flag = 1
    # number表示尝试次数
    # 其他都和研究生打卡过程一样，具体注释看研究生打卡
    number = 0
    for i in range(len(username_list)):
        while True:
            try:
                browser = driver()
                time.sleep(3)
                username = username_list[i]
                password = password_list[i]
                log_in(browser, username, password)
                dangshi(browser=browser)
                time.sleep(5)
                temp(browser)
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

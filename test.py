from splinter.browser import Browser
from time import sleep
from wxpy import *


bot=Bot()
my_friend = bot.friends().search('冠军')[0]
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
# initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"#购票页面
orderList_url = "https://kyfw.12306.cn/otn/view/train_order.html"#订单页面
onlinepay_url = "https://kyfw.12306.cn/otn//payOrder/init"#订单完成页面
payment_url = "https://mrexcashier.alipay.com/index.htm"#支付页面

order = 0  #车次，0代表所有车次，依次从上到下
user = ["倪明"]#乘客姓名，若购学生票记得在姓名后面加括号
seatType = 3 #1为商务座，2为一等座，3为二等座，以此类推


driver = Browser(driver_name='chrome')
driver.driver.set_window_size(1400, 1000)#设置打开的浏览器的窗口尺寸

def login():
    driver.visit(login_url)
    # 填充密码
    driver.fill("loginUserDTO.user_name", '980855285@qq.com')  # 后面为12306账号
    driver.fill("userDTO.password", 'yan521680')  # 后面为密码
    # driver.fill("loginUserDTO.user_name", '18401610488')#后面为12306账号
    # driver.fill("userDTO.password", 'qazwsx110120119')#后面为密码
    print('''\n\n**********************
**等待验证码，自行输入**
**********************''')
    while True:
        if driver.url != initmy_url:
            sleep(2)
        else:
            break

def payment():
    driver.visit(orderList_url)

    try:
        sleep(2)
        driver.find_by_text("去支付").click()
        sleep(6)
        driver.find_by_id("payButton").click()
        sleep(2)
        driver.windows.current=driver.windows[1]
        sleep(1)
        driver.find_by_xpath("/html/body/div[2]/div[2]/div/form/div[9]/div/img").click()
        sleep(2)
        while True:
            if payment_url in driver.url:
                screenshotURL = driver.screenshot("D:/PyCharm 2018.2.4/workspace/LearnPy/learn/GetTickets/screen.png")
                screenshotName = screenshotURL.split('\\')[-1]
                print('网页截图的名字：')
                print(screenshotName)
                # my_friend.send('Hello!')
                # my_friend.send_image(screenshotName)
                break
    except Exception as e:
        print(e)

def book_ticket(ticket_url):
    driver.visit(ticket_url)
    try:
        print("-------开始刷票-------")
        # 加载查询信息
        driver.cookies.add({"_jc_save_fromStation": "%u5317%u4EAC%2CBJP"})#北京
        driver.cookies.add({"_jc_save_toStation": "%u5A7A%u6E90%2CWYG"})#婺源
        driver.cookies.add({"_jc_save_fromDate": "2018-11-30"})

        sleep(1)
        driver.reload()
        #driver.select("cc_start_time", "18002400")
        #该方法可以下拉菜单中选择时段，但是select标签没有name属性，使用id属性没有成功

        #时间段选择
        # driver.find_by_id("cc_start_time").click()
        # driver.find_option_by_value("06001200").click()

        count = 0
        if order != 0:
            while driver.url == ticket_url:
                driver.find_by_text("查询").click()
                count += 1
                print(" \r -----第{}次刷新-----" .format(count))
                try:
                    driver.find_by_text("预订")[order - 1].click()
                except Exception as e:
                    print(e)
                    print("尚未开始预订")
                    continue
        else:
            while driver.url == ticket_url:
                driver.find_by_text("查询").click()
                count += 1
                print(" \r -----第{}次刷新-----" .format(count))
                try:
                    js='var tbody=document.querySelector("#queryLeftTable");var array = tbody.getElementsByTagName("tr");' \
                       'var index=new Array();' \
                       'for(var i = 0; i < array.length/2; i++) {' \
                       'var tds = array[i*2].children;' \
                       'var tag=tds['+seatType+'].innerHTML;' \
                       'if(tag!="<div>无</div>"&&tag!="--")' \
                       '{' \
                       'tds['+seatType+'].innerHTML="有票";' \
                       'index.push(i);' \
                       '}' \
                       '};' \
                       'document.getElementById("fromStationText_label").innerHTML = index;' \
                    # driver.execute_script('document.getElementById("fromStationText_label").innerHTML = "meto";')
                    sleep(2)
                    driver.execute_script(js)
                    print(driver.find_by_id('fromStationText_label')[0].value)
                    indexArr=driver.find_by_id('fromStationText_label')[0].value.split(',')
                    orderButtons=driver.find_by_text("预订")
                    for i in indexArr:
                        print(i)
                        orderButtons[int(i)].click()
                        sleep(2)
                except Exception as e:
                    print(e)
                    print("尚未开始预订")
                    continue
        print("\n\n****开始预订****")
        print('\n>>>开始选择用户')
        for u in user:
            driver.find_by_text(u).last.click()

        print("\n---> ^^提交订单")
        sleep(1)
        driver.find_by_id('submitOrder_id').click()
        sleep(1)
        print("确认选座...")
        driver.find_by_id('qr_submit_id').click()
        # 支付部分
        while True:
            if onlinepay_url in driver.url:
                sleep(8)
                print("开始支付...")
                driver.find_by_id("payButton").click()
                break
        sleep(2)
        driver.windows.current=driver.windows[1]
        sleep(1)
        driver.find_by_xpath("/html/body/div[2]/div[2]/div/form/div[9]/div/img").click()
        sleep(2)
        while True:
            if payment_url in driver.url:
                screenshotURL = driver.screenshot("D:/PyCharm 2018.2.4/workspace/LearnPy/learn/GetTickets/screen.png")
                screenshotName = screenshotURL.split('\\')[-1]
                print('网页截图的名字：')
                print(screenshotName)
                my_friend.send('Hello!')
                my_friend.send_image(screenshotName)
                break
    except Exception as e:
        print(e)

def main():
    login()
    # payment()
    book_ticket(ticket_url)
main()
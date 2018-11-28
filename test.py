from splinter.browser import Browser
from time import sleep

login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
# initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"#购票页面

order = 0  #车次，0代表所有车次，依次从上到下
user = ["郎垿峰"]#乘客姓名，若购学生票记得在姓名后面加括号

driver = Browser(driver_name='chrome')
driver.driver.set_window_size(1400, 1000)#设置打开的浏览器的窗口尺寸

def login():
    driver.visit(login_url)
    # 填充密码
    driver.fill("loginUserDTO.user_name", '18401610488')#后面**为12306账号
    driver.fill("userDTO.password", 'qazwsx110120119')#后面**为密码
    print('''\n\n**********************
**等待验证码，自行输入**
**********************''')
    while True:
        if driver.url != initmy_url:
            sleep(1)
        else:
            break

def book_ticket(ticket_url):
    driver.visit(ticket_url)
    try:
        print("-------开始刷票-------")
        # 加载查询信息
        driver.cookies.add({"_jc_save_fromStation": "%u5317%u4EAC%2CBJP"})#北京
        driver.cookies.add({"_jc_save_toStation": "%u5A7A%u6E90%2CWYG"})#婺源
        driver.cookies.add({"_jc_save_fromDate": "2018-12-15"})

        sleep(2)
        driver.reload()
        #driver.select("cc_start_time", "18002400")
        #该方法可以下拉菜单中选择时段，但是select标签没有name属性，使用id属性没有成功

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
                    for i in driver.find_by_text("预订"):
                        i.click()
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


    except Exception as e:
        print(e)

def main():
    login()
    book_ticket(ticket_url)
main()
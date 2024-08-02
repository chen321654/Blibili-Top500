import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from lxml import etree
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

class Blibli:
    def __init__(self, url):
        self.driver = self.start_browser(url)


    def start_browser(self, url):
        self.driver = webdriver.Edge()
        self.driver.get(url)
    
        return self.driver

    def save_csv(self, data):
        df = pd.DataFrame(data)
        df.to_excel("Blibli热门视频.xlsx", index=False, engine='openpyxl')

    def login(self, username, passwd):
        # 鼠标悬停到登录
        icon = self.driver.find_element(By.XPATH, '//ul[@class="right-entry"]//div[@class="header-login-entry"]')
        actions = ActionChains(self.driver)
        actions.move_to_element(icon).perform()
    
        # login_icon = self.driver.find_element(By.XPATH, '//div[@class="v-popover is-bottom"]//div[@class="login-btn"]')
    
    
        login_icon = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="bili-mini-login-right-wp"]/div[2]/form/div[1]/input'))
        )
        login_icon.click()
    
        username_in = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="bili-mini-login-right-wp"]/div[2]/form/div[1]/input'))
        ).send_keys(username)
    
        passwd_in = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="login-pwd-wp"]//div[@class="form__item"]/input[@placeholder="请输入密码"]'))
        ).send_keys(passwd)
    
        login = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="btn_wp"]/div[2]'))
        ).click()
        input("输入任意继续....")
    
    def get_hot_research(self):
    
        hot_search = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="bili-header__channel"]/div/a[2]'))
        ).click()
    
        # 切换到新窗口
        self.driver.switch_to.window(self.driver.window_handles[-1])
    
    
        name_ele = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="popular-video-container popular-list"]/div[@class="flow-loader"]/ul'))
        )
    
        # 滚动页面直到元素出现
        target_xpath = '//div[@class="no-more"]'  # 替换为你要查找的元素的 XPath
        mark = False
        scroll_pause_time = 2

        while True:
            if mark:
                break
            # 检查目标元素是否出现
            try:
                element = WebDriverWait(self.driver, scroll_pause_time).until(
                    EC.presence_of_element_located((By.XPATH, target_xpath))
                )
                mark = True
                print("Element found:", element.text)
                break
            except:
                # 向下滚动
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause_time)
        else:
            print("Element not found after max scrolls")

        all_infos = self.driver.find_element(By.XPATH,  '//div[@class="popular-video-container popular-list"]/div[@class="flow-loader"]/ul')

        title = all_infos.find_elements(By.XPATH, './/div/div[2]/p')
        view_num = all_infos.find_elements(By.XPATH, './/div/div[2]/div[1]/p/span[1]')
        comment_num = all_infos.find_elements(By.XPATH, './/div/div[2]/div[1]/p/span[2]')

        data = {
            "视频名称": [i.text for i in title],
            "播放量": [i.text for i in view_num],
            "评论数": [i.text for i in comment_num]
        }

        # data = {
        #     "title": title,
        #     "view_num": view_num,
        #     "comment_num": comment_num
        # }
        return data
        # print(len(name))
        # for i in range(len(name)):
        #
        #     print(name[i].text, view_num[i].text, comment_num[i].text)


if __name__ == '__main__':
    url = "https://www.bilibili.com"
    # username = 'bili_92817948019'
    # passwd = "3600739Qaz."

    blibli = Blibli(url)
    data = blibli.get_hot_research()

    blibli.save_csv(data)
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import cv2
import numpy as np
import urllib.request as request
import scrapy
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


class SkinsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SkinsDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='skins/driver/chromedriver.exe')
        self.driver.implicitly_wait(20)
        self.wait = WebDriverWait(self.driver, 10)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(1)
        if spider.name == "buff":
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'iframe')))
            btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.u-tab.f-cb a")))
            btn.click()

            uname = self.wait.until(EC.element_to_be_clickable((By.ID, "phoneipt")))
            uname.clear()
            uname.click()
            uname.send_keys("18961712890")
            time.sleep(0.3)
            password = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "j-inputtext")))
            password.clear()
            password.click()
            password.send_keys("PYF686999@@")

            self.verifySlideCode()
            btn = self.wait.until(EC.element_to_be_clickable((By.ID, "submitBtn")))
            btn.click()
            time.sleep(1)
            self.driver.switch_to.parent_frame()
            time.sleep(1)

        html = self.driver.page_source
        return scrapy.http.HtmlResponse(url=self.driver.current_url, body=html.encode('utf-8'), encoding="UTF-8")

    def clickVerifyBtn(self):
        verify_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "btnCertificationpone")))
        verify_btn.click()

    def slideVerifyCode(self):
        slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_slider')))
        ActionChains(self.driver).click_and_hold(slider).perform()
        slider_loc_x = slider.location["x"]
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "yidun_bg-img")))
        icon = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "yidun_jigsaw")))
        pic_width = img.size['width']
        icon_width = icon.size['width']
        img_tags = self.driver.find_elements_by_tag_name("img")
        img_url = img_tags[0].get_attribute("src")
        icon_url = img_tags[1].get_attribute("src")
        match_x = self.distance(img_url, icon_url, pic_width)
        if match_x == -1:
            raise Exception()

        slider_instance = self.getSlideInstance(pic_width, icon_width, match_x)
        tracks = self.get_tracks(slider_instance)

        for track in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
        else:
            ActionChains(self.driver).move_by_offset(xoffset=3, yoffset=0).perform()
            ActionChains(self.driver).move_by_offset(xoffset=-1, yoffset=0).perform()
            ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()
            time.sleep(0.5)
            ActionChains(self.driver).release().perform()
        time.sleep(1)
        cur_loc_x = slider.location["x"]
        if cur_loc_x > slider_loc_x:
            print("success")
            return True
        else:
            return False

    def verifySlideCode(self, attempt_times=10):
        # 尝试attempt_times次滑动验证，返回是否验证通过
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "yidun_tips__text"), r"向右拖动滑块填充拼图"))
        for attempt in range(attempt_times):
            try:
                if self.slideVerifyCode():
                    return True
            except Exception as e:
                print(e)
                ActionChains(self.driver).release().perform()
                refresh = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "yidun_refresh")))
                refresh.click()
                time.sleep(0.6)
        return False

    def mathc_img(self, img_gray, template, value):
        # 图标和原图的匹配位置，即为图标要移动的距离
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = value
        loc = np.where(res >= threshold)
        result_size = len(loc[1])
        if result_size > 0:
            middle = round(result_size / 2)
            '''
            #show match result
            guess_points = zip(*loc[::-1])
            for pt in guess_points:
                cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 1)
            cv2.imshow('Detected', img_gray)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            '''
            return loc[1][middle]

        else:
            return -1

    def cropHeight(self, icon):
        mid = round(icon.shape[1] / 2)
        c = icon[:, mid, 2]
        no0 = np.where(c != 0)
        first, last = no0[0][0], no0[0][-1]
        return first, last

    def loadImg(self, url):
        resp = request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image

    def cropImage(self, img, top_y, bottom_y):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        crop_img = img_gray[top_y:bottom_y, :]
        return crop_img

    def showImg(self, img, name):
        cv2.imshow(name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def distance(self, img_url, icon_url, display_width):
        value = 0.45
        img_rgb = self.loadImg(img_url)
        tmp_rgb = self.loadImg(icon_url)
        crop_height = self.cropHeight(tmp_rgb)
        pic = self.cropImage(img_rgb, *crop_height)
        icon = self.cropImage(tmp_rgb, *crop_height)
        src_width = img_rgb.shape[1]
        guess_px = self.mathc_img(pic, icon, value)

        if guess_px is not -1:
            return round(guess_px * display_width / src_width)
        else:
            return -1

    # copy demo
    def get_tracks(self, distance):
        """
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式：
        ①v=v0+at
        ②s=v0t+½at²
        ③v²-v0²=2as

        :param distance: 需要移动的距离
        :return: 存放每0.3秒移动的距离
        """
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.3
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 4 / 5

        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = 2
            else:
                a = -3
                # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))

            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t
        return tracks

    def getSlideInstance(self, img_w, icon_w, match_x):
        # 考虑到滑块和图标的速度不总是1:1,获取滑块实际滑动的距离
        slider_width = 40
        iconMslider = icon_w - slider_width
        first_l = round(iconMslider / 2)
        mid_l = img_w - first_l
        # end_l = img_w - first_l - mid_l  #eliminate 1px error
        if match_x <= first_l:
            return match_x * 2
        elif match_x <= first_l + mid_l:
            return match_x + first_l
        else:
            return 2 * match_x - mid_l

# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time

user = "712937709"
pwd = "RTX990802@@"

chrome_options = Options()
chrome_options.add_argument('headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

driver.get("http://act.ff.sdo.com/20180707jifen/index.html#/home")
time.sleep(1)
btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.signBtn")))
btn.click()
time.sleep(1)
btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.wegame_icon")))
btn.click()
time.sleep(1)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, 'ptlogin_iframe')))
btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a#switcher_plogin.link")))
btn.click()
time.sleep(1)
uname = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#u")))
uname.clear()
uname.click()
uname.send_keys(user)
time.sleep(0.3)
password = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#p")))
password.clear()
password.click()
password.send_keys(pwd)
btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.login_button")))
btn.click()
time.sleep(3)
wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="app"]/div[2]/div/div[1]/span'), '请选择角色'))
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/form/div[1]/div/div/div[1]/input').send_keys(Keys.ENTER)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/form/div[1]/div/div/div[1]/input').send_keys(Keys.ARROW_DOWN,
                                                                                                            Keys.ARROW_DOWN,
                                                                                                            Keys.ENTER)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[2]/form/div[2]/div/div/div[1]/input').send_keys(Keys.ENTER,
                                                                                                            Keys.ARROW_DOWN,
                                                                                                            Keys.ENTER)
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div[3]/div/button[2]').click()
time.sleep(1)
btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/div/div/div[3]')))
btn.click()
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.el-notification__content')))
p = driver.find_element_by_css_selector('div.el-notification__content p').text
print(p)

print('Success')
input()

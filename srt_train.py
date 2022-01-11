import http
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import re
import requests
from bs4 import BeautifulSoup as bs, Comment
import cx_Oracle
import os
import logging
import uuid
import urllib
import cgi

os.environ['NLS_LANG'] = '.UTF8'  # UnicodeEncodeError

logger = logging.getLogger('rnd_crawling')
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)

options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 헤드리스모드
options.add_argument('--disable-gpu')  # 호환성용 (필요없는 경우도 있음)
options.add_argument('--window-size=1920x1080')  # (가상)화면 크기 조절
options.add_argument('--no-sandbox')  # 보안 해제 설정
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
options.binary_location = 'C://Program Files/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome('./chromedriver/chromedriver', options=options)
driver.set_page_load_timeout(120)  # selenium timeout 120초

try:
    logger.debug('예매 로그인사이트로 이동합니다.')
    driver.get('https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000')
    time.sleep(5)
    id = '2088936200'
    pw = '357159!ansdlsqh'
    tag_id = driver.find_element_by_name('srchDvNm').send_keys(id)
    tag_pw = driver.find_element_by_name('hmpgPwdCphd').send_keys(pw)
    log_in_go = '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input'
    driver.find_element_by_xpath(log_in_go).click()
    logger.debug('로그인이 정상적으로 되었습니다.')
    logger.debug('예약 사이트로 이동합니다.~')
    time.sleep(5)
    driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000')

    round_trip_button = '//*[@id="chtnDvCd3"]'
    driver.find_element_by_xpath(round_trip_button).click()
    round_trip_site_go = driver.switch_to_alert()
    round_trip_site_go.accept()

    depart_location = '평택지제'
    arrive_location = '부산'
    driver.find_element_by_name('dptRsStnCdNm').clear()
    driver.find_element_by_name('arvRsStnCdNm').clear()
    tag_depart_location = driver.find_element_by_name('dptRsStnCdNm').send_keys(depart_location)
    tag_arrive_location = driver.find_element_by_name('arvRsStnCdNm').send_keys(arrive_location)
    Lookup_button = '#search_top_tag > input'
    driver.find_element_by_css_selector(Lookup_button).click()
    # driver.quit()
    # print('브라우저 quit')
except TimeoutException as e:
    print('시간 초과')
except Exception as e1:
    print('다른오류')
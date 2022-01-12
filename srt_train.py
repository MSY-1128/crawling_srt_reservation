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
# options.add_argument('--window-size=1920x1080')  # (가상)화면 크기 조절
options.add_argument('--start-fullscreen')  # (가상)화면 크기 조절
options.add_argument('--no-sandbox')  # 보안 해제 설정
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
options.binary_location = 'C://Program Files/Google/Chrome/Application/chrome.exe'
driver = webdriver.Chrome('./chromedriver/chromedriver', options=options)
driver.set_page_load_timeout(120)  # selenium timeout 120초

try:
    logger.debug('예매 로그인사이트로 이동합니다.')
    driver.get('https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000')
    time.sleep(1)
    id = '???'
    pw = '???'
    tag_id = driver.find_element_by_name('srchDvNm').send_keys(id)
    tag_pw = driver.find_element_by_name('hmpgPwdCphd').send_keys(pw)
    log_in_go = '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input'
    driver.find_element_by_xpath(log_in_go).click()
    logger.debug('로그인이 정상적으로 되었습니다.')
    logger.debug('예약 사이트로 이동합니다.~')


    driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000')

    round_trip_button = '//*[@id="chtnDvCd3"]'
    driver.find_element_by_xpath(round_trip_button).click()
    round_trip_site_go = driver.switch_to_alert()
    round_trip_site_go.accept()

    depart_location = '평택지제'
    arrive_location = '부산'
    start_date = '//*[@id="dptDt1"]/option[15]'  # 테스트로 출발날짜 2022/01/21 지정
    comback_date = '//*[@id="dptDt2"]/option[17]'  #  테스트로 돌아오는 날짜 2022/01/03으로 지정
    start_time = '//*[@id="dptTm1"]/option[8]'
    comback_time = '//*[@id="dptTm2"]/option[8]'

    driver.find_element_by_name('dptRsStnCdNm').clear()
    driver.find_element_by_name('arvRsStnCdNm').clear()
    tag_depart_location = driver.find_element_by_name('dptRsStnCdNm').send_keys(depart_location)
    tag_arrive_location = driver.find_element_by_name('arvRsStnCdNm').send_keys(arrive_location)

    driver.find_element_by_xpath(start_date).click()
    driver.find_element_by_xpath(comback_date).click()
    driver.find_element_by_xpath(start_time).click()
    driver.find_element_by_xpath(comback_time).click()



    Lookup_button = '#search_top_tag > input'
    driver.find_element_by_css_selector(Lookup_button).click() # 조회버튼


    time.sleep(1)
    start_reservation = '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[1]/td[7]/a'
    comback_reservation = '//*[@id="result-form"]/fieldset/div[13]/table/tbody/tr[1]/td[7]/a'
    driver.find_element_by_xpath(start_reservation).click()
    driver.find_element_by_xpath(comback_reservation).click()

    # time.sleep(1)
    # reservation_finish = '//*[@id="result-form"]/fieldset/div[19]/input[2]'
    # driver.find_element_by_xpath(reservation_finish).click()


except TimeoutException as e:
    print('시간 초과')
except Exception as e1:
    logger.error('########## Selenium 작동이 중지 되었습니다 : %s' % e1)
    raise Exception(e1)

# finally:
    # driver.quit()
    # print('브라우저 quit')
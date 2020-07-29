from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
import time
import json

import logging
import sys
logging.basicConfig(stream=sys.stdout, 
format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

SLEEP_TIME = 240
def getCourse(course_name, options_course):
    for coruse in options_course.options:
        if(coruse.text[:len(course_name)] == course_name):
            return coruse.text
    print('course input error')
    exit(0)

def getPostion(position_name, options_pos):
    for position in options_pos.options:
        if(position.text[:len(position_name)] == position_name):
            return position.text
    print('position input error')
    exit(0)

def getDate(date_name, options_date):
    for date in options_date.options:
        if(date.text[:len(date_name)] == date_name):
            return date.text
    print('date input error')
    exit(0)

LOGIN_URL = 'https://bookseat.tkblearning.com.tw/book-seat/student/login/toLogin'

def bookTKB():
    driverLocation = '/home/ray/Desktop/python/parser/chromedriver'
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(executable_path=driverLocation, chrome_options=options) # 選擇Chrome瀏覽器
    driver.set_window_size(480, 600)

    with open('/home/ray/Desktop/python/parser/config.json', 'r') as f:
        config = json.load(f)

    st = time.time()
    print('===start===', st - st)
    driver.get(LOGIN_URL)
    connect_time = time.time()
    print('===connected===', connect_time - st)

    driver.find_element_by_id('id').click()
    driver.find_element_by_id('pwd').click()


    driver.find_element_by_link_text('送出').click()

    get_submit_alert, sleep_times = False, 0
    while(not get_submit_alert):
        if sleep_times >= SLEEP_TIME:
            print('no alert in login')
            exit(0)
        sleep_times += 1
        try:
            alogin = driver.switch_to_alert()
            print(alogin.text)
            alogin.accept()
            get_submit_alert = True
        except NoAlertPresentException:
            time.sleep(1)
            pass


    #time.sleep(2)
    into_book_page, sleep_times = False, 0
    while(not into_book_page):
        if sleep_times >= SLEEP_TIME:
            print('fail to login')
            exit(0)
        sleep_times += 1
        try:
            driver.find_element_by_css_selector("select[id='class_selector']")
            into_book_page = True
        except NoSuchElementException:
            time.sleep(1)
            pass

    into_time = time.time()
    print('===into_time===', into_time - st)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    select_course = driver.find_element_by_css_selector("select[id='class_selector']")
    options_course = Select(select_course)
    course_name = getCourse(config["course"], options_course)
    options_course.select_by_visible_text(course_name)
    print(course_name)

    select_date = driver.find_element_by_css_selector("select[id='date_selector']")
    options_date = Select(select_date)
    date_name = getDate(config["date"], options_date)
    options_date.select_by_visible_text(date_name)
    print(date_name)

    select_branch = driver.find_element_by_css_selector("select[id='branch_selector']")
    options_branch = Select(select_branch)
    position_name = getPostion(config["position"], options_branch)
    options_branch.select_by_visible_text(position_name)
    print(position_name)

    all_checkboxs=driver.find_elements_by_css_selector('input[type=checkbox]')
    disabled_checkboxs=driver.find_elements_by_css_selector('input[type=checkbox][disabled]')
    abled_checkboxs = [a for a in all_checkboxs if a not in disabled_checkboxs]

    checked = False
    for idx, checkbox in enumerate(all_checkboxs):
        if idx + 1 == 3:
            continue
        if checkbox in abled_checkboxs:
            checkbox.click()
            checked = True
            break

    if not checked:
        print('no more session')
        exit(0)

    ed = time.time()
    print('===end===', ed - st)
    driver.save_screenshot('/home/ray/Desktop/python/parser/test.png')
    driver.find_element_by_link_text('送出').click()

    ### Todo: sleep and wait for the alert
    get_submit_alert, sleep_times = False, 0
    while(not get_submit_alert):
        if sleep_times >= SLEEP_TIME:
            print('fail to confirm submit')
            exit(0)
        sleep_times += 1
        try:
            abook = driver.switch_to_alert()
            print(abook.text)
            abook.accept()
            get_submit_alert = True
        except NoAlertPresentException:
            time.sleep(1)
            pass

    get_submit_alert, final_sleep_times = False, 0
    while(not get_submit_alert):
        if(final_sleep_times >= SLEEP_TIME):
            print('No final alert')
            exit(0)
        final_sleep_times += 1
        try:
            afinal = driver.switch_to_alert()
            print(afinal.text)
            afinal.accept()
            get_submit_alert = True
        except NoAlertPresentException:
            time.sleep(1)
            pass

    ### Todo: try 5 times until succeed with function call
    ### Todo: scheduling and get config each trial
    ### Todo: put the root directory of program into config

if __name__ == '__main__':
    logging.warning('[TKB booking...]')
    bookTKB()
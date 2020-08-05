from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
import datetime, time
import json

#from apscheduler.scheduler import Scheduler
from apscheduler.schedulers.blocking import BlockingScheduler

import logging
import sys
import os
logging.basicConfig(stream=sys.stdout, 
format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

try:
    with open('access.json', 'r') as f:
        access = json.load(f)
        USERID = access['USERID']
        PASSWORD = access['PASSWORD']
        DRIVERLOCATION = access['DRIVERLOCATION']
except:
    logging.warning('Please Add access json')
    exit(0)

SLEEP_TIME = 240
REST_THRESHOLD = 600
TIME_DELTA = 0
def getCourse(course_name, options_course):
    for coruse in options_course.options:
        if(coruse.text[:len(course_name)] == course_name):
            return coruse.text
    logging.warning('course input error')
    return False

def getPostion(position_name, options_pos):
    for position in options_pos.options:
        if(position.text[:len(position_name)] == position_name):
            return position.text
    logging.warning('position input error')
    return False

def getDate(date_name, options_date):
    for date in options_date.options:
        if(date.text[:len(date_name)] == date_name):
            return date.text
    logging.warning('date input error')
    return False

def checkInPage(driver):
    #time.sleep(2)
    into_book_page, sleep_times = False, 0
    while(not into_book_page):
        if sleep_times >= SLEEP_TIME:
            return False
        sleep_times += 1
        try:
            driver.find_element_by_css_selector("select[id='class_selector']")
            into_book_page = True
            return True
        except NoSuchElementException:
            time.sleep(1)

def checkInLogin(driver):
    login, sleep_times = False, 0
    while(not login):
        if sleep_times >= SLEEP_TIME:
            return False
        sleep_times += 1
        try:
            driver.find_element_by_id('id')
            login = True
            return True
        except NoSuchElementException:
            time.sleep(1)

def getConfig():
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    return config

def bookTKB(mode='Normal'):
    logging.warning('[TKB booking...]')

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    #options.binary_location = GOOGLE_CHROME_BIN

    driver = webdriver.Chrome(executable_path=DRIVERLOCATION, chrome_options=options) # 選擇Chrome瀏覽器
    driver.set_window_size(400, 1800)

    ### get config
    config = getConfig()
    print(config)

    st = time.time()
    logging.warning('=== start {} ==='.format(st - st))
    driver.get(LOGIN_URL)
    connect_time = time.time()
    logging.warning('=== connected {} ==='.format(connect_time - st))

    islogin = checkInLogin(driver)
    if not islogin:
        logging.warning('fail to login')
        driver.quit()
        return False

    driver.find_element_by_id('id').click()
    driver.find_element_by_id('id').send_keys(USERID)
    driver.find_element_by_id('pwd').click()
    driver.find_element_by_id('pwd').send_keys(PASSWORD)
    driver.find_element_by_link_text('送出').click()

    get_submit_alert, sleep_times = False, 0
    while(not get_submit_alert):
        if sleep_times >= SLEEP_TIME:
            logging.warning('no alert in login')
            driver.quit()
            return False
        sleep_times += 1
        try:
            alogin = driver.switch_to_alert()
            print(alogin.text)
            alogin.accept()
            get_submit_alert = True
        except NoAlertPresentException:
            time.sleep(1)
            pass

    inCoursePage = checkInPage(driver)
    if not inCoursePage:
        logging.warning('fail to in course page')
        driver.quit()
        return False

    
    logging.warning('=== into_time ===')
    today = datetime.datetime.now()
    if today < datetime.datetime(today.year, today.month, today.day, 12 - TIME_DELTA, 0, 0):
        # morning, booking noon
        rest_time = (datetime.datetime(today.year, today.month, today.day, 12 - TIME_DELTA, 0, 0) - today).total_seconds() + 1
    else:
        # afternoon, booking midnight
        rest_time = (datetime.datetime(today.year, today.month, today.day, 23 - TIME_DELTA, 59, 59) - today).total_seconds() + 2
    
    if mode == 'Cron':
        if rest_time > REST_THRESHOLD or rest_time < 0:
            logging.warning('something wrong on rest')
            driver.quit()
            return False

    driver.save_screenshot('login.png')
    
    logging.warning('[sleeping {} minutes...]'.format(rest_time / 60))
    time.sleep(rest_time)
    logging.warning('[wake up and clean refresh course...]')

    ### push clear
    driver.find_element_by_link_text('清除').click()

    clearCoursePage = checkInPage(driver)
    if not clearCoursePage:
        logging.warning('fail to clear course page')
        driver.quit()
        return False

    driver.save_screenshot('clear.png')

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    select_course = driver.find_element_by_css_selector("select[id='class_selector']")
    options_course = Select(select_course)
    course_name = getCourse(config["course"], options_course)
    if not course_name:
        driver.quit()
        return False
    options_course.select_by_visible_text(course_name)
    logging.warning(course_name)

    select_date = driver.find_element_by_css_selector("select[id='date_selector']")
    options_date = Select(select_date)
    date_name = getDate(config["date"], options_date)
    if not date_name:
        driver.quit()
        return False
    options_date.select_by_visible_text(date_name)
    logging.warning(date_name)

    select_branch = driver.find_element_by_css_selector("select[id='branch_selector']")
    options_branch = Select(select_branch)
    position_name = getPostion(config["position"], options_branch)
    if not position_name:
        driver.quit()
        return False
    options_branch.select_by_visible_text(position_name)
    logging.warning(position_name)

    has_class=driver.find_elements_by_css_selector('input[type=checkbox][value=hasClass]')
    
    if len(has_class) != 0:
        logging.warning('You already have seat')
        driver.quit()
        return False

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

    driver.save_screenshot('test.png')

    if not checked:
        logging.warning('no more session')
        driver.quit()
        return False

    ed = time.time()
    logging.warning('=== end {} ==='.format(ed - st))
    driver.find_element_by_link_text('送出').click()

    ### Todo: sleep and wait for the alert
    get_submit_alert, sleep_times = False, 0
    while(not get_submit_alert):
        if sleep_times >= SLEEP_TIME:
            print('fail to confirm submit')
            driver.quit()
            return False
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
            driver.quit()
            return False
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
    driver.quit()
    return True

def printHello():
    print('hello')
    return

def main():
    logging.warning('running...')
    bookTKB('Normal')

def main_schedule():
    sched = BlockingScheduler()

    sched.add_job(bookTKB, trigger='cron', hour=23, minute=50, args=('Cron',))
    sched.add_job(bookTKB, trigger='cron', hour=11, minute=50, args=('Cron',))
    logging.warning('running...')
    sched.start()

import argparse
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--schedule", help="if using schedule",
        action="store_true")
    args = parser.parse_args()

    LOGIN_URL = 'https://bookseat.tkblearning.com.tw/book-seat/student/login/toLogin'

    if args.schedule:
        main_schedule()
    else:
        main()
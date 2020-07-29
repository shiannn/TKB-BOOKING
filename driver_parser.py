from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
import time

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

driverLocation = './chromedriver'
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=driverLocation, chrome_options=options) # 選擇Chrome瀏覽器
driver.set_window_size(1024, 960)

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
    #if sleep_times >= 8:
    #    print('no alert in login')
    #    exit(0)
    #sleep_times += 1
    try:
        alogin = driver.switch_to_alert()
        print(alogin.text)
        alogin.accept()
        get_submit_alert = True
    except NoAlertPresentException:
        #time.sleep(1)
        pass

driver.save_screenshot('test.png')
#time.sleep(2)
into_book_page, sleep_times = False, 0
while(not into_book_page):
    #if sleep_times >= 8:
    #    print('fail to login')
    #    exit(0)
    #sleep_times += 1
    try:
        driver.find_element_by_css_selector("select[id='class_selector']")
        into_book_page = True
    except NoSuchElementException:
        #time.sleep(1)
        pass

into_time = time.time()
print('===into_time===', into_time - st)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

select_course = driver.find_element_by_css_selector("select[id='class_selector']")
options_course = Select(select_course)
course_name = getCourse('資料結構', options_course)
options_course.select_by_visible_text(course_name)
print(course_name)

select_date = driver.find_element_by_css_selector("select[id='date_selector']")
options_date = Select(select_date)
date_name = getDate('2020-07-29', options_date)
options_date.select_by_visible_text(date_name)
print(date_name)

select_branch = driver.find_element_by_css_selector("select[id='branch_selector']")
options_branch = Select(select_branch)
position_name = getPostion('公館', options_branch)
options_branch.select_by_visible_text(position_name)
print(position_name)

all_checkboxs=driver.find_elements_by_css_selector('input[type=checkbox]')
disabled_checkboxs=driver.find_elements_by_css_selector('input[type=checkbox][disabled]')
abled_checkboxs = [a for a in all_checkboxs if a not in disabled_checkboxs]
for checkbox in abled_checkboxs:
    #checkbox.click()
    #print(checkbox.is_selected())
    if not checkbox.is_selected():
        checkbox.click()
        break

ed = time.time()
print('===end===', ed - st)
exit(0)
driver.find_element_by_link_text('送出').click()

get_submit_alert = False
while(not get_submit_alert):
    try:
        abook = driver.switch_to_alert()
        print(abook.text)
        abook.accept()
        get_submit_alert = True
    except NoAlertPresentException:
        pass

get_submit_alert, final_sleep_times = False, 0
while(not get_submit_alert):
    if(final_sleep_times >= 5):
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

#time.sleep(2)
#driver.switch_to_alert().accept()
#time.sleep(2)
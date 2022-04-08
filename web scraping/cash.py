from asyncio.windows_events import NULL
from http.client import CONTINUE
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://www.investing.com/indices/usdollar")
try:
    time.sleep(1)
    accept_popup = driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    #time.sleep(2)
    #wait = WebDriverWait(driver,30)
    #try to move mouse
    #if  wait.until(EC.presence_of_element_located((By.ID, "PromoteSignUpPopUp"))) != NULL:
       #time.sleep(1)
       #elemlist2 = driver.find_element(By.CLASS_NAME, "popupCloseIcon largeBannerCloser").click()
    #    wait.until(EC.visibility_of_element_located((By.ID, "PromoteSignUpPopUp")))
    #    driver.find_element(By.XPATH, '//*[@id="PromoteSignUpPopUp"]/div[2]/i').click()
   
    #if driver.find_element(By.CLASS_NAME, "popupCloseIcon largeBannerCloser") is not NULL:
   
    #time.sleep(5)
    driver.find_element(By.LINK_TEXT, "Historical Data").click()
    #time.sleep(1)
    #elemlist2 = driver.find_element(By.CLASS_NAME, "popupCloseIcon largeBannerCloser")
    #elemlist2.click()

    ## CALENDAR
    # load calendar
    time.sleep(1)
    driver.find_element(By.ID, "flatDatePickerCanvasHol").click()
    #time.sleep(1)
    sel_startDate = driver.find_element(By.XPATH,'//*[@id="startDate"]')
    sel_startDate.clear()
    sel_startDate.send_keys("01/01/2020")
    # endDate
    sel_endDate = driver.find_element(By.XPATH,'//*[@id="endDate"]')
    sel_endDate.clear()
    sel_endDate.send_keys("12/31/2020")
    driver.find_element(By.XPATH,'//*[@id="applyBtn"]').click()
    time.sleep(1)
    
    table = driver.find_element(By.ID,'curr_table')
    with open('../data/with_blank_cash.csv', 'w') as csvfile:
        wr = csv.writer(csvfile)
        for row in table.find_elements(By.CSS_SELECTOR,'tr'):
            wr.writerow([d.text for d in row.find_elements(By.CSS_SELECTOR,'th')])
            wr.writerow([d.text for d in row.find_elements(By.CSS_SELECTOR,'td')])
    df = pd.read_csv('../data/with_blank_cash.csv')
    df.to_csv('../data/usdollar.csv', index = False)


finally :
    driver.close()
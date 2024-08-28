# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains

from seleniumbase import webdriver
from seleniumbase.webdriver.common.by import By
from seleniumbase.webdriver.support.ui import WebDriverWait
from seleniumbase.webdriver.support import expected_conditions as EC
from seleniumbase.webdriver.common.action_chains import ActionChains

import time
from datetime import datetime
from datetime import timedelta
import os
import streamlit as st

# Username and password stored in separate file
#username = login_details.username
#password = login_details.password

def export_bookings():
    username = 'akhilesh.bhat-external@westwing.de'
    password = 'HSELihka2024!'
    url = "https://login.transporeon.com/?locale=en_US#RetailTSM/bookingoverview.html"
    
    # Set browser preferences
    st.write(os.getcwd())
    prefs = {
        "download.default_directory": os.getcwd(),
        "download.directory_upgrade": True,
        "download.prompt_for_download": False,
    }
    ChrOptions = webdriver.ChromeOptions()
    ChrOptions.add_experimental_option("prefs", prefs)
    ChrOptions.add_argument('--headless=new')
    
    # Select webdriver (chrome, edge, etc.)
    driver = webdriver.Chrome(options=ChrOptions)
    driver.get(url)
    driver.maximize_window()   # Open the Website and maximize window
    
    wait = WebDriverWait(driver, 10)
    actionChains = ActionChains(driver)
    
    
    #whenever driver.action doesn't work, use wait.until(EC.element_to_be_clickable/visible).action
    # Enter username & password, and then press sign-in
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="emailForm_email-input"]'))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="emailForm_password-input"]'))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="emailForm_submit"]'))).click()
    
    i = 0
    page_not_loaded =True
    st.write('loading iframes')
    while page_not_loaded:          # the booking overview takes a while to load. Hence the while loop
        try:
            driver.switch_to.frame("iFrameRetailTSM")       #Lesson : the elements are within an iframe. so need to switch into it
            page_not_loaded = False
        except:
            i = i+1
            time.sleep(3)        
    
    page_not_loaded =True
    while page_not_loaded:          # the booking overview takes a while to load. Hence the while loop
        try:
            driver.switch_to.frame("mclegacy")       #Lesson : the elements are within an iframe. so need to switch into it
            page_not_loaded = False
        except:
            i = i+1
            time.sleep(3)      
        
    # driver.switch_to.frame("mclegacy")  #Switch into the the iframe within the iframe
    time.sleep(3)

    st.write('updating warehouse/date filters')
    # Selecting the warehouses
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ext-gen98"]'))).click()  #Click on dropdown
    wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[7]/div/div[4]'))).click()   #Deselect the 4th option - ELC5 returns
    
    # Selecting the warehouse gates
    # No code here for now
    
    #Select start date
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ext-gen21_DATEFIELDTRIGGER"]'))).click()  #Click on dropdown. Here clicking on the calendar icon works
    start_date = datetime.strftime(datetime.today() + timedelta(days=-1),"%b %d, %Y").replace(" 0"," ")
    # print('//*[@title="'+ start_date +'"]')
    elem=driver.find_element(By.XPATH, '//*[@title="'+ start_date +'"]')
    wait.until(EC.element_to_be_clickable(elem)).click()
    
    #Select end date
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ext-gen24_DATEFIELDTRIGGER"]'))).click()  #Click on dropdown. Here clicking on the calendar icon works
    end_date = datetime.strftime(datetime.today() + timedelta(days=3),"%b %d, %Y").replace(" 0"," ")
    
    # we do the below loop because once the start date is selected, there are two elements in the html with the same date value (one in the start-date form and one in end-date form)
    elems=driver.find_elements(By.XPATH, '//*[@title="'+ end_date +'"]')
    for element in elems:
        try:
            element.click()
        except:
            pass
    
    #Click on load report
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ext-gen181"]'))).click() 
    
    
    #Export the report
    elem = driver.find_element(By.XPATH,'//*[@id="ext-gen202"]')
    driver.execute_script("arguments[0].scrollIntoView();", elem)
    driver.execute_script("arguments[0].click();", elem)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Bookings + purchase orders"]'))).click() 
    
    #doing the below loop because there are two 'Export' buttons. First in the overview page, then the actual export button.
    elems=driver.find_elements(By.XPATH, '//button[text()="Export"]')    
    for element in elems:
        try:
            element.click()
            time.sleep(5)
        except:
            pass    
    #driver.switchTo().defaultContent();  to switch out of the iframe   
    
    driver.close()
    driver.quit()

if __name__ == '__main__':
    export_bookings()

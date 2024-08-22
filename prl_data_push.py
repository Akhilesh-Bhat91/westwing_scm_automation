from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import os
import streamlit as st
# Username and password stored in separate file
#username = login_details.username
#password = login_details.password


def po_placement(allPOData_df):
    username = 'a.bhat-x'
    password = 'QYE2gxd-kju0kz!'
    # Select webdriver (chrome, edge, etc.)
    driver = webdriver.Chrome()

    # Open the Website and maximize window
    driver.get("https://mono.westwing.eu/")#put here the adress of your page
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)
    actionChains = ActionChains(driver)

    # Click on login button (to get xpath, righ click on button > inspect > right click on highlighted text > xpath)
    #driver.find_element('xpath','//*[@id="page"]/div[2]/div/div[2]/form/button').click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@class='btn-large btn-block btn-onelogin']"))).click()

    #whenever driver.action doesn't work, use wait.until(EC.element_to_be_clickable/visible)
    # Enter username and click continue

    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div[3]/form/div/div[3]/div/button'))).click()

    # Enter password and click continue
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div[3]/form/div/div[4]/div/button'))).click()

    # Select role
    actionChains.move_to_element(wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='user_roleSelectorDropdown__2G36I']")))).perform()
    cur_role = wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='user_roleSelectorDropdown__2G36I']/span"))).text

    if cur_role != "PRL user":
        wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='user_roleSelectorDropdown__2G36I']/ul/li[contains(text(),'PRL user')]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@class='btn-large btn-block btn-onelogin']"))).click()


    # allPOData_df = pd.read_excel("WWC_Input_Sample.xlsx")
    poList = allPOData_df['PO Number'].unique()
    pack_dict = {'Neutral':'1','Westwing Collection':'2','Branded':'3','Mixed':'4'}
    potype_dict = {'DDP':'2','FOB':'3','FOB External':'4'}
    warehouse_dict = {'ELC5':'1','ELC7':'3'}
    address_dict = {'ELC5':'2','ELC7':'4'}
    original_window = driver.current_window_handle
    for po in poList:

        # Click purchase orders  
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-item-purchase-orders"]'))).click()
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)            
                break
        cur_window = driver.current_window_handle
        
        # if len(driver.window_handles)==2:
        #     driver.close()
        #     driver.switch_to().window(driver.window_handles[0])

        # print('no. of handles: ',len(driver.window_handles))
        
        # Click create PO
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="create-new-po-btn"]'))).click()
        
        #get all data for the specific PO
        poData = allPOData_df[allPOData_df['PO Number'] == po]
        poClipData = poData.reindex(columns = ['Westwing SKU','Supplier SKU','Product Name','Fragility Index','ETA Date','FOB Date','Initial Price','Item Qty']) 
        # poClipData = poData[['Westwing SKU','Supplier SKU',	'Product Name','Fragility Index','ETA Date','FOB Date','Initial Price','Item Qty']]
        poClipData.to_clipboard(excel=True, header=False, index=False)
        poType = poData['PO Type'].unique()[0]
        warehouse = poData['Warehouse'].unique()[0]
        packaging = poData['Packaging'].unique()[0]
        cbm = poData['CBM'].unique()[0]
        skuList = poData['Westwing SKU'].tolist()
        etaList = poData['ETA Date'].dt.date.tolist()
        fobList = poData['FOB Date'].dt.date.tolist()
        qtyList = poData['Item Qty'].tolist()
        scmName = poData['SCM'].unique()[0]
        currency = poData['Currency'].unique()[0]

        #select PO type
        popath = '/html/body/div[2]/div/div[2]/section/div/section[2]/div/ul/li['+ potype_dict[poType] + ']'
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dialog-po-type-dropdown"]'))).click()    #select dropdown
        wait.until(EC.element_to_be_clickable((By.XPATH, popath))).click() 

        #select warehouse
        wpath = '/html/body/div[2]/div/div[2]/section/div/section[1]/div/ul/li['+ warehouse_dict[warehouse] +']'
        
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dialog-logistics-provider-dropdown"]'))).click()    
        wait.until(EC.element_to_be_clickable((By.XPATH, wpath ))).click()
        
        #select currency    
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dialog-currency-dropdown"]'))).click()  
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()=\''+ currency +'\']'))).click()  

        if poType == 'FOB' or poType == 'DDP':
            #select packaging
            driver.find_element('xpath','//*[@id="dialog-private-label-packaging-input"]').click() #select dropdown
            driver.find_element('xpath','/html/body/div[2]/div/div[2]/section/div/section[8]/div/ul/li[1'+ pack_dict[packaging] +']').click() 
            #enter cbm
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dialog-private-label-cbm-input"]'))).send_keys(cbm)
        
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/nav/button[2]'))).click()

        
        # Select Delivery Adress
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div/section[3]/div[1]/div/div[1]/div/div[2]'))).click() 
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div/section[3]/div[1]/div/div[1]/div/div[2]/ul/li['+ address_dict[warehouse] +']/div/span'))).click()

        # Need to check how to select the right SCM contact. Not all contacts are there
        # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div[1]/div/section[3]/div[1]/div/div[1]/div/div[3]'))).click() # open dropdown
        # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()=\''+ scmName +'\']'))).click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") #scroll down. Script fails on laptop if this line is skipped (works instead on big desktop, even without this line)
        field = driver.find_element('xpath','//*[@id="products"]/div[1]/div/div/div/table/tbody/tr/td[3]')
        # actionChains.double_click(field).perform()
        # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="products"]/div[5]/textarea'))).send_keys(skuOutput)
        ActionChains(driver).move_to_element(field).click(field).key_down(Keys.CONTROL).send_keys('v').perform()
        driver.execute_script("window.scrollTo(0,0)") #scroll up
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="po-detail-btn-update"]'))).click()  #click update
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="po-detail-btn-save"]'))).click()    #click save    
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="po-detail-btn-approved"]'))).click() #click approve
        print(wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="po-detail-info-bar-number"]'))).text)
        input()
        if cur_window != original_window:
            driver.close()
            driver.switch_to.window(original_window)
        # input('Press <ENTER> to continue')

if __name__ == '__main__':
    po_placement()


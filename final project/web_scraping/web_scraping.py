#!/usr/bin/env python3
"""
This file contains all the code implementation corresponding to the part 1 of the project.
The code below, through webscraping on the web page https://www.investing.com/ obtains 5 datasets corresponding to 5 desired assets (depending on the parameters introduced by the user).

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os


class ObtainCSVFilesFromWeb():
    """
    This class allows to create different datasets using web scraping.
    """
    def __init__(self, web_browser: str, web_page: str):
        """
        Init ObtainCSVFilesFromWeb. Initialize the web browser options and the web page from which the information is to be extracted.
        
        Args:
            web_browser (str): 
                A string represents the web browser.
            web_page (str):
                A string represents the URL to the web page.
        """
        
        self.web_page = web_page
        if web_browser == "Chrome":
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--log-level=1")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920x1080")
            self.driver = webdriver.Chrome(options=chrome_options)
    
    
    def create_datasets_from_investing(self, folder_path: str, dataset_name: str):
        """
        Using webscraping, this function create a csv file(s) in "folder_path" folder.
        
        Args:
            folder_path (str):
                A string indicating the path to the folder where the csv file(s) is to be saved.
            dataset_name (str): 
                A string representing the csv file to be created. It can take one of the following values: 
                 - "All" to create all datasets.
                 - "Stocks" to create amundi-msci-wrld-ae-c.csv
                 - "Corporate bonds" to create ishares-global-corporate-bond-$.csv
                 - "Public bonds" to create db-x-trackers-ii-global-sovereign-5.csv
                 - "Golds" to create spdr-gold-trust.csv
                 - "Cash" to create usdollar.csv         
        """
        
        assetsid_stockmarket = {
            "0P00012PP6":"Fund - Luxembourg fund", 
            "CRPS":"ETF - London etf", 
            "XG7S":"ETF - Milan etf", 
            "US78463V1070":"ETF - NYSE etf", 
            "US Dollar Index (DXY)":"Index - NYSE"
        }
        assetsid_csvname = {
            "0P00012PP6":"amundi-msci-wrld-ae-c.csv", 
            "CRPS":"ishares-global-corporate-bond-$.csv", 
            "XG7S":"db-x-trackers-ii-global-sovereign-5.csv", 
            "US78463V1070":"spdr-gold-trust.csv", 
            "US Dollar Index (DXY)":"usdollar.csv"
        }
        datasets_available = {"Stocks":["CRPS", "XG7S", "US78463V1070", "US Dollar Index (DXY)"], 
                              "Corporate bonds":["0P00012PP6", "US Dollar Index (DXY)", "XG7S", "US78463V1070"],
                              "Public bonds":["0P00012PP6", "CRPS", "US78463V1070", "US Dollar Index (DXY)"],
                              "Golds":["0P00012PP6", "CRPS", "XG7S", "US Dollar Index (DXY)"], 
                              "Cash":["0P00012PP6", "CRPS", "XG7S", "US78463V1070"]
        }   
        # Parameter checking.
        try:
            assert dataset_name == "All" or dataset_name in datasets_available.keys(), f"\033[1m ERROR: \033[0m Please, select a valid .csv file, '{dataset_name}' not available."
        except AssertionError as error:
            print(error)
            exit(1)
        
        if dataset_name in datasets_available.keys():
            datasets_available = datasets_available.pop(dataset_name)
            for elem in datasets_available:
                del assetsid_stockmarket[elem]
                
        driver = self.driver
        driver.get(self.web_page)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click() # Closing popup.

            for asset_code, stockmarket in assetsid_stockmarket.items():
                # Write the asset code in the searcher line.
                driver.find_element(by=By.TAG_NAME, value="INPUT").send_keys(asset_code) 
                # Search button.
                driver.find_element(by=By.TAG_NAME, value="LABEL").click() 
                # Select desired asset.
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, stockmarket))).click() 
                # Historical data button.
                driver.find_element(by=By.LINK_TEXT, value="Historical Data").click() 
                # Opening calendar.
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "widgetFieldDateRange"))).click() 
                # Modify startDate value.
                start_date_search_bar = driver.find_element(by=By.ID, value="startDate") 
                start_date_search_bar.clear()
                start_date_search_bar.send_keys("01/01/2020") 
                # Modify endDate value.
                end_date_search_bar = driver.find_element(by=By.ID, value="endDate")
                end_date_search_bar.clear()
                end_date_search_bar.send_keys("12/31/2020")
                # Applying date changes to the calendar.
                driver.find_element(by=By.ID, value="applyBtn").click()
                # Wait until the table is available.
                html_table = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "curr_table"))) 
                # Table to html form.
                df_html = pd.read_html(html_table.get_attribute("outerHTML"), index_col=0) 
                # Table html to pandas DataFrame.
                df = pd.DataFrame(df_html[0]).drop(["Open", "High", "Low"], axis=1).convert_dtypes() 
                # For US Dolar, compute the value of 1 US dolar for that day.
                if asset_code == "US Dollar Index (DXY)": df["Price"] = round(pd.to_numeric(df["Price"])/100, 3)
                
                if os.path.isdir(folder_path) == False: os.mkdir(folder_path) 
                   
                df.to_csv(path_or_buf= folder_path + "/" + assetsid_csvname[asset_code]) 

        finally :
            driver.close() 
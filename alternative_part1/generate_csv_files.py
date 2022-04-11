"""
This file contains all the code implementation corresponding to the part 1 of the project.
The code below, through webscraping on the web page https://www.investing.com/ obtains 5 datasets corresponding to 5 desired assets.
The datasets are generated in the directory 'csv_files'.

To run the code in terminal: python3 generate_csv_files.py <route_to_csv_store_folder> <name_csv_to_create>
<route_to_csv_store_folder>: -> route in which the user want to spawn the csv files
<name_csv_to_create>: choose between the following values -> All or Stocks or Corporate bonds or Public bonds or Golds or Cash
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import sys


class ObtainCSVFilesFromWeb():
    """
    This class allows to create different datasets using webscraping.
    """
    def __init__(self, web_browser: str, web_page: str):
        """
        Init ObtainCSVFilesFromWeb. Initialize the web browser options and the web page from which the information is to be extracted.
        
        Args:
            web_browser (str): 
                A string representing the web browser.
            web_page (str):
                A string representing the URL to the web page.
        """
        # Checking parameter values
        assert isinstance(web_browser, str), "web_browser variable must be string type" 
        assert isinstance(web_page, str), "web_page variable must be string type"
        assert web_browser == "Chrome", f"web_browser variable must be 'Chrome', {web_browser} is not allowed"

        self.web_page = web_page
        # driver = Chrome or Firefox depending on the value of the web_browser parameter
        if web_browser == "Chrome":
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            # chrome_options.add_argument("--no-sandbox")
            # chrome_options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=chrome_options)
    
    def create_datasets_from_investing(self, path_to_folder: str, dataset: str):
        """
        Using webscraping, this function create a csv file(s) in "path_to_folder" folder.
        
        Args:
            path_to_folder (str):
                A string indicating the path to the folder where the csv file(s) is to be saved.
            dataset (str): 
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
        assert self.web_page == "https://www.investing.com/", f"web_page must be 'https://www.investing.com/', {self.web_page} is not valid for this function"
        
        datasets_available = ["All", "Stocks", "Corporate bonds", "Public bonds", "Golds", "Cash"]
        
        if dataset not in datasets_available: exit(f"Please, select a valid dataset, '{dataset}' not available") 
            
        if dataset == datasets_available[1]:
            del assetsid_stockmarket["CRPS"], assetsid_stockmarket["XG7S"], assetsid_stockmarket["US78463V1070"], assetsid_stockmarket["US Dollar Index (DXY)"]
        elif dataset == datasets_available[2]:
            del assetsid_stockmarket["0P00012PP6"], assetsid_stockmarket["XG7S"], assetsid_stockmarket["US78463V1070"], assetsid_stockmarket["US Dollar Index (DXY)"]
        elif dataset == datasets_available[3]:
            del assetsid_stockmarket["0P00012PP6"], assetsid_stockmarket["CRPS"], assetsid_stockmarket["US78463V1070"], assetsid_stockmarket["US Dollar Index (DXY)"]
        elif dataset == datasets_available[4]:
            del assetsid_stockmarket["0P00012PP6"], assetsid_stockmarket["CRPS"], assetsid_stockmarket["XG7S"], assetsid_stockmarket["US Dollar Index (DXY)"]
        elif dataset == datasets_available[5]:
            del assetsid_stockmarket["0P00012PP6"], assetsid_stockmarket["CRPS"], assetsid_stockmarket["XG7S"], assetsid_stockmarket["US78463V1070"]
        
        driver = self.driver
        driver.get(self.web_page)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click() # Closing popup

            for asset_code, stockmarket in assetsid_stockmarket.items():
                # Write the asset code in the searcher line 
                driver.find_element(by=By.TAG_NAME, value="INPUT").send_keys(asset_code) 
                # Search button
                driver.find_element(by=By.TAG_NAME, value="LABEL").click() 
                # Select desired asset 
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, stockmarket))).click() 
                # Historical data button
                driver.find_element(by=By.LINK_TEXT, value="Historical Data").click() 
                # Opening calendar
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "widgetFieldDateRange"))).click() 
                # Modify startDate value
                start_date_search_bar = driver.find_element(by=By.ID, value="startDate") 
                start_date_search_bar.clear()
                start_date_search_bar.send_keys("01/01/2020") 
                # Modify endDate value
                end_date_search_bar = driver.find_element(by=By.ID, value="endDate")
                end_date_search_bar.clear()
                end_date_search_bar.send_keys("12/31/2020")
                # Applying date changes to the calendar
                driver.find_element(by=By.ID, value="applyBtn").click()
                # Wait until the table is available
                html_table = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "curr_table"))) 
                # Table to html form
                df_html = pd.read_html(html_table.get_attribute('outerHTML'), index_col=0) 
                # Table html to pandas DataFrame
                df = pd.DataFrame(df_html[0]).drop(["Open", "High", "Low"], axis=1).convert_dtypes() 
                # For US Dolar, compute the value of 1 US dolar for that day
                if asset_code == "US Dollar Index (DXY)": df["Price"] = pd.to_numeric(df["Price"])/100 
                    
                if os.path.isdir(f"{path_to_folder}") == False: os.mkdir(f"{path_to_folder}") 
                   
                df.to_csv(path_or_buf=f"{path_to_folder}/{assetsid_csvname[asset_code]}") # DataFrame to csv file

        finally :
            driver.close() 

    
if __name__ == "__main__":
    ObtainCSVFilesFromWeb(web_browser='Chrome', web_page='https://www.investing.com/').create_datasets_from_investing(path_to_folder=sys.argv[1], dataset=sys.argv[2])
    
    
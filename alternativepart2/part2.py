#!/usr/bin/env python3
from itertools import product
import pandas as pd
import os
import numpy as np
import re

class Portfolio():
    """
    This class allows to create a portfolio and also clean datasets from web scraping part.
    """
    def __init__(self, assets: str, increment_decrement: float=20.0):
        """
        Init Portfolio. Sets the increase/decrease of the portfolio and the assets from which I want to create the portfolio. 
        
        Args:
            assets (str):
                A string that contains the acronyms of the different assets from which the portfolio is to be created.
            increment_decrement (float): 
                A float that represent the increase/decrease of the portfolio. By default = 20.0 (see exercise statement).
            
        """
        
        assert increment_decrement > 0 and increment_decrement < 101, "Increment/decrement value must be higher than 1 and less than 101"
        self.increment_decrement = increment_decrement 
        available_assets = ["ST", "CB", "PB", "GO", "CA"]
        param_list_assets = list(assets.split(" "))
        unique_assets = list(set([asset for asset in param_list_assets if asset in available_assets]))
        self.assets = [asset for asset in available_assets if asset in unique_assets]
        assert len(self.assets) >= 1, "The assets selected are not available"
        
    def generate_portfolio_allocations_csv(self, path_to_folder: str):
        """
        Create portfolio allocations in the route specified in path_to_folder parameter and returns it as pd.DataFrame object.
        
        Args:
            path_to_folder (str): 
                A string indicating the path to the folder where the csv file is to be saved.
        Returns:
            pd.DataFrame object which is the portfolio allocations.
        """
        
        weights = list(range(0, 101, self.increment_decrement))
        generate_portfolios = sorted(product(weights, repeat=len(self.assets)), reverse=True)
        portfolio_allocations = pd.DataFrame([portfolio for portfolio in list(generate_portfolios) if sum(portfolio) == 100], columns=self.assets)
        if os.path.isdir(f"{path_to_folder}") == False: os.mkdir(f"{path_to_folder}")
        portfolio_allocations.to_csv(path_or_buf=f"{path_to_folder}/portfolio_allocations.csv", index=False)
        
        return portfolio_allocations
        
        
    def treat_csv_files(self, path_to_folder: str):
        """
        Treat the csv files from web scraping part stored in path_to_folder route.
        
        Args:
            path_to_folder (str): 
                A string indicating the path where are the csv files from web scraping part.
        Returns:
            dict: 
                - Key: the acronyms of the different assets.
                - Value: a pd.DataFrame object which is the processed csv corresponding to the asset.
        """
        
        # We see if exists the web scraping csv files hat we want to treat from the assets that we want to create the portfolio.
        asset_csv_names = {"ST":"amundi-msci-wrld-ae-c.csv", "CB":"ishares-global-corporate-bond-$.csv", "PB":"db-x-trackers-ii-global-sovereign-5.csv", "GO":"spdr-gold-trust.csv", "CA":"usdollar.csv"}
        remove_keys = [asset for asset in asset_csv_names.keys() if asset not in self.assets]
        for asset in remove_keys: del asset_csv_names[asset] 
        path_csvs_availables = [f"{path_to_folder}/{csv_name}" for _, csv_name in asset_csv_names.items() if os.path.exists(f"{path_to_folder}/{csv_name}")] 
        if len(asset_csv_names) != len(path_csvs_availables): exit("Error, the csv files of the desired assets are not available in the specified path")
        csvs_treated = {}
        type_asset_index = 0
        # Modify each csv file if it exist
        for csv_file in path_csvs_availables:
    
            df = pd.read_csv(csv_file)
            # Date to str
            df["Date"] = pd.to_datetime(df["Date"])
            df["Date"] = df["Date"].dt.date
            df["Date"] = df["Date"].apply(lambda x: str(x))
            # Col name changed and % character deleted
            df = df.rename(columns={"Change %": "Change"})
            df["Change"] = pd.to_numeric(df["Change"].apply(lambda x: x.replace("%", "")))
            # Missing dates
            missing_dates = pd.date_range(start='2020-01-01', end='2020-12-31').difference(df["Date"])
            missing_dates_df = pd.DataFrame(missing_dates.strftime('%Y-%m-%d'), columns=["Date"])
            # For new dates, columns "Price" and "Change" are assigned the average of each column
            avg_price = df["Price"].mean()
            missing_dates_df["Price"] = round(avg_price, 2)
            avg_change = df["Change"].mean()
            missing_dates_df["Change"] = round(avg_change, 2)
            # If "Vol." column in pd.DataFrame then replace "K" (1e+3), "M" (1e+6) and "-" characters by mean of the column. The missing date rows the same
            if "Vol." in df.columns:
                df = df.rename(columns={"Vol.": "Vol"})
                units_val = {"K":1e+3, "M":1e+6}
                    
                for unit, val in units_val.items():
                    if "Vol" in df.columns and df["Vol"].dtype == "O" and df["Vol"].str.contains(unit).any():
                        if df["Vol"].str.contains("-").any():
                            df["Vol"] = df["Vol"].apply(lambda x: pd.to_numeric(x.replace(unit, ""))*val if unit in x else np.nan)
                            avg_vol = round(df["Vol"][~np.isnan(df["Vol"])].mean(), 3)
                            df["Vol"] = df["Vol"].fillna(avg_vol)
                            missing_dates_df["Vol"] = avg_vol
                        else:
                            df["Vol"] = df["Vol"].apply(lambda x: pd.to_numeric(x.replace(unit, ""))*val)
                            avg_vol = round(df["Vol"].mean(), 3)
                            missing_dates_df["Vol"] = avg_vol
                      
            complete_dataframe = pd.concat([missing_dates_df, df], ignore_index=True).sort_values(by="Date").reset_index(drop=True).dropna(axis=1)
            csvs_treated[self.assets[type_asset_index]] = complete_dataframe
            type_asset_index += 1
            
        return csvs_treated



    def generate_portfolio_metrics_csv(path_to_folder: str, treat_csv_files: dict, portfolio_allocations: pd.DataFrame,  money_invested: float, purchase_date: str="2020-01-01"):
        """
        Create portfolio metrics in path_to_folder route.
        
        Args:
            path_to_folder (str): 
                A string indicating the path to the folder where the csv file is to be saved.
            treat_csv_files (dict):
                A dictionary in wich the key is the acronym of the asset and the value the treat csv in pd.DataFrame format.
            portfolio_allocations (pd.DataFrame):
                The portfolio allocations generated previously in pd.DataFrame format.
            money_invested (float):
                A float that indicates the amount of money that SAM want to invest.
            purchase_date (str):
                The date from which you want to calculate metrics. By default = "2020-01-01" (see exercise statement)
        """
        
        # ST,CB,PB,GO,CA,RETURN,VOLAT
        # ST --> Stocks --> amundi-msci-wrld-ae-c.csv|| CB --> Corporate bonds --> ishares-global-corporate-bond-$.csv 
        # PB --> Public bonds --> db-x-trackers-ii-global-sovereign-5.csv || GO --> Gold --> spdr-gold-trust.csv || CA --> Cash --> usdollar.csv 
    
        # Parameter checking
        if money_invested <= 0: exit("The money to be invested must be greater than 0")
        match = re.search("^(2020)(-)(0[1-9]|1[0-2])(-)(0[1-9]|1[0-9]|2[0-9]|3[0-1])$", purchase_date)
        if match == None: exit("Date format is not correct, the format must be the following: YYYY-MM-DD")
        if purchase_date in ["2020-02-30", "2020-02-31"]: exit("The introduced date does not exist")
        
        allocations = portfolio_allocations.to_dict("list")
        asset_money_invested = {}
        asset_current_val = {}
        for asset in portfolio_allocations.columns:
            # Calculating RETURN column
            df_asset = treat_csv_files[asset]
            purchase_price = float(df_asset[df_asset["Date"].astype("string") == purchase_date]["Price"])
            current_price = float(df_asset[df_asset["Date"].astype("string") == "2020-12-31"]["Price"]) 
            bj_num_assets = [(((money_invested*alloc)/100)/purchase_price) if alloc != 0 else 0.0 for alloc in allocations[asset]] 
            asset_money_invested[asset] = [num_share*purchase_price for num_share in bj_num_assets]
            asset_current_val[asset] = [num_share*current_price for num_share in bj_num_assets]
            # TODO: Calculating VOLATILITY column
            
        buy_amount = pd.DataFrame(asset_money_invested).sum(axis=1)
        current_value = pd.DataFrame(asset_current_val).sum(axis=1)
        portfolio_allocations["RETURN"] = round(((current_value - buy_amount)/buy_amount) * 100, 3)
                   
        portfolio_allocations.to_csv(path_or_buf="/home/rafael/Desktop/2nd_quarter/PythonCourse/final_assignment/part2/portfolios_csv/RETURN.csv", index=0)           
                   
                   
                   
                   
                   
                   
                   
                   
        # if os.path.isdir(f"{path_to_folder}") == False: os.mkdir(f"{path_to_folder}")     
        # df.to_csv(path_or_buf=f"{path_to_folder}/portfolio_metrics.csv") # DataFrame to csv file

if __name__ == "__main__":
    
    
    # increment_decrement = float(input("Please, write the value for the increment/decrement (the project statement recommends either 20 or 0.2, but it could be another one): "))
    # if increment_decrement < 1.0: increment_decrement *= 100
        
    # increment_decrement = int(increment_decrement)
    # assets = input("Please, write the assets from which you want to create the portfolio without quotes and separated by spaces ('ST' 'CB' 'PB' 'GO' 'CA'): ")
    # path_to_folder_portfolio = input("Please, type the route when you want spawn portfolio_allocations.csv files: ")
    # path_to_folder_csv_from_webscraping = input("Please, type the path where the csv files \033[1m from webscraping part \033[0m are located: ")
    
    portfolio = Portfolio(increment_decrement=20, assets="ST CB PB GO CA") #increment_decrement=increment_decrement, assets=assets
    portfolio_allocations = portfolio.generate_portfolio_allocations_csv(path_to_folder="part2/portfolios_csv") # path_to_folder=path_to_folder_portfolio
    clean_webscraping_csv_files = portfolio.treat_csv_files(path_to_folder="part1/csv_files") # path_to_folder=path_to_folder_csv_from_webscraping
    
    portfolio.generate_portfolio_metrics_csv(treat_csv_files=clean_webscraping_csv_files, portfolio_allocations=portfolio_allocations, money_invested=10000, purchase_date="2020-01-01")
    # print(clean_webscraping_csv_files["ST"])
    # print(clean_webscraping_csv_files["CB"])
    # print(clean_webscraping_csv_files["PB"])
    # print(clean_webscraping_csv_files["GO"])
    # print(clean_webscraping_csv_files["CA"])

    # print(clean_webscraping_csv_files.keys())

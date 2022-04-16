#!/usr/bin/env python3
"""
This file contains all the code implementation corresponding to the part 2 of the project.
The code below, generate portfolios, treat the csv files from web scraping part and generate metrics (return, volatility) for each portfolio.
"""
from itertools import product
import pandas as pd
import os
import numpy as np
import re


class Portfolio():
    """
    This class allows to create a portfolio and also clean datasets from web scraping part.
    """
    def __init__(self, folder_path: str, assets: str, increment_decrement: float=20.0):
        """
        Init Portfolio. Sets the increase/decrease of the portfolio and the assets from which I want to create the portfolio. 
        
        Args:
            folder_path (str): 
                A string indicating the path to the folder where the csv file is to be saved.
            assets (str):
                A string that contains the acronyms of the different assets from which the portfolio is to be created.
            increment_decrement (float): 
                A float that represent the increase/decrease of the portfolio. By default = 20.0 (see exercise statement).
        """
        
        self.folder_path = folder_path
        if os.path.isdir(self.folder_path) == False: os.mkdir(self.folder_path)
        self.increment_decrement = increment_decrement 
        available_assets = ["ST", "CB", "PB", "GO", "CA"]
        param_list_assets = list(assets.split(" "))
        unique_assets = list(set([asset for asset in param_list_assets if asset in available_assets]))
        self.assets = [asset for asset in available_assets if asset in unique_assets]
        # Parameter checking.
        try:
            assert increment_decrement > 0 and increment_decrement < 101, "\033[1m ERROR: \033[0m Increment/decrement value must be higher than 1 and less than 101"
            assert len(self.assets) >= 1, f"\033[1m ERROR: \033[0m At least on of the assets selected ({assets}) are not available."
        except AssertionError as error:
            print(error)
            exit(1)
            
        
    def generate_portfolio_allocations_csv(self):
        """
        Create portfolio allocations in the route specified in folder_path parameter and returns it as pd.DataFrame object.
        
        Args:
            folder_path (str): 
                A string indicating the path to the folder where the csv file is to be saved.
        Returns:
            pd.DataFrame object which is the portfolio allocations.
        """
        
        weights = list(range(0, 101, self.increment_decrement))
        generate_portfolios = sorted(product(weights, repeat=len(self.assets)), reverse=True)
        portfolio_allocations = pd.DataFrame([portfolio for portfolio in list(generate_portfolios) if sum(portfolio) == 100], columns=self.assets)
        
        portfolio_allocations.to_csv(path_or_buf= self.folder_path + "/portfolio_allocations.csv", index=False)
        
        return portfolio_allocations
        
        
    def treat_csv_files(self, web_scraping_csv_folder_path: str):
        """
        Treat the csv files from web scraping part stored in folder_path route.
        
        Args:
            web_scraping_csv_folder_path (str): 
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
        path_csvs_availables = [web_scraping_csv_folder_path + "/" + csv_name for _, csv_name in asset_csv_names.items() if os.path.exists(web_scraping_csv_folder_path + "/" + csv_name)] 
        
        # Parameter checking.
        try:
            assert len(asset_csv_names) == len(path_csvs_availables), "\033[1m ERROR: \033[0m The csv files for all desired assets are not available in the specified path"
        except AssertionError as error:
            print(error)
            exit(1)
        
        csvs_treated = {}
        type_asset_index = 0
        # Modify each csv file if it exist.
        for csv_file in path_csvs_availables:
    
            df = pd.read_csv(csv_file)
            # Date to str.
            df["Date"] = pd.to_datetime(df["Date"])
            df["Date"] = df["Date"].dt.date
            df["Date"] = df["Date"].apply(lambda x: str(x))
            # Col name changed and % character deleted.
            df = df.rename(columns={"Change %": "Change"})
            df["Change"] = pd.to_numeric(df["Change"].apply(lambda x: x.replace("%", "")))
            # Missing dates
            missing_dates = pd.date_range(start='2020-01-01', end='2020-12-31').difference(df["Date"])
            missing_dates_df = pd.DataFrame(missing_dates.strftime('%Y-%m-%d'), columns=["Date"])
            # For new dates, columns "Price" and "Change" are assigned the average of each column.
            avg_price = df["Price"].mean()
            missing_dates_df["Price"] = round(avg_price, 2)
            avg_change = df["Change"].mean()
            missing_dates_df["Change"] = round(avg_change, 2)
            # If "Vol." column in pd.DataFrame then replace "K" (1e+3), "M" (1e+6) and "-" characters by mean of the column. The missing date rows the same.
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


    def generate_portfolio_metrics_csv(self, treat_csv_files: dict, portfolio_allocations: pd.DataFrame, purchase_date: str="2020-01-01"):
        """
        Create portfolio metrics in folder_path route.
        
        Args:
            treat_csv_files (dict):
                A dictionary in wich the key is the acronym of the asset and the value the treat csv in pd.DataFrame format.
            portfolio_allocations (pd.DataFrame):
                The portfolio allocations generated previously in pd.DataFrame format.
            purchase_date (str):
                The date from which you want to calculate metrics. By default = "2020-01-01" (see exercise statement)
        """

        # Parameter checking.
        match = re.search("^(2020)(-)(0[1-9]|1[0-2])(-)(0[1-9]|1[0-9]|2[0-9]|3[0-1])$", purchase_date)
        try:
            assert match != None, "\033[1m ERROR: \033[0m The date selected is not available or date format is not correct, the format must be the following: YYYY-MM-DD"
            assert purchase_date not in ["2020-02-30", "2020-02-31", "2020-04-31", "2020-06-31", "2020-09-31", "2020-11-31"], "\033[1m ERROR: \033[0m The introduced date does not exist."
        except AssertionError as error:
            print(error)
            exit(1)
        
        money_invested = 10000 # This value really does not matter.
        allocations = portfolio_allocations.to_dict("list")
        asset_money_invested, asset_current_val, asset_values = {}, {}, {}
 
        for asset in portfolio_allocations.columns:
            
            df_asset = treat_csv_files[asset]
            # RETURN.
            # Price initial date.
            purchase_price = float(df_asset[df_asset["Date"].astype("string") == purchase_date]["Price"])
            # Price last date.
            current_price = float(df_asset[df_asset["Date"].astype("string") == "2020-12-31"]["Price"]) 
            # Number of shares.
            bj_num_shares = [(((money_invested*alloc)/100)/purchase_price) if alloc != 0 else 0.0 for alloc in allocations[asset]] 
            # Buy amount and current value for each asset.
            asset_money_invested[asset] = [num_share*purchase_price for num_share in bj_num_shares]
            asset_current_val[asset] = [num_share*current_price for num_share in bj_num_shares]
            # VOLATILITY.
            # Prices for all days since purchase date (included).
            prices = list(df_asset[df_asset["Date"].astype('string') >= purchase_date]["Price"])
            # Calculating sharesji * priceji for all assets for all days for in all portfolios.
            asset_values[asset] = np.array([np.array([num_shares*price for price in prices]) for num_shares in bj_num_shares]).T # Numpy is faster (implemented in C++)

        # Valuei final calculation, (sum of matrix asset_values[asset]).
        days_portfolio_prices = 0
        for i in list(asset_values.values()):
            days_portfolio_prices += i
        df_prices_evol = pd.DataFrame(days_portfolio_prices) # Rows=days Cols=portfolios.
        # RETURN parameters.    
        buy_amount = pd.DataFrame(asset_money_invested).sum(axis=1)
        current_value = pd.DataFrame(asset_current_val).sum(axis=1)
        # VOLATILITY parameters.
        std_dev = df_prices_evol.std(axis=0)
        sample_avg = df_prices_evol.mean(axis=0)
        # Final calculation of RETURN and VOLATILITY.
        portfolio_allocations["RETURN"] = round(((current_value-buy_amount)/buy_amount)*100, 3)
        portfolio_allocations["VOLAT"] = round((std_dev/sample_avg)*100, 3)   
        
        portfolio_allocations.to_csv(path_or_buf= self.folder_path + "/portfolio_metrics.csv", index=0)           
#!/usr/bin/env python3
from itertools import product
import pandas as pd
import os
import numpy as np

class Portfolio():
    
    def __init__(self, increment_decrement: float, assets: str):
        assert increment_decrement > 0 and increment_decrement < 101, "Increment/decrement value must be higher than 1 and less than 101"
        self.increment_decrement = increment_decrement 
        available_assets = ["ST", "CB", "PB", "GO", "CA"]
        param_list_assets = list(assets.split(" "))
        unique_assets = list(set([asset for asset in param_list_assets if asset in available_assets]))
        self.assets = [asset for asset in available_assets if asset in unique_assets]
         
        
        assert len(self.assets) >= 1, "The assets selected are not available"
        
    def generate_portfolio_allocations_csv(self, path_to_folder: str):
        """
        Create portfolio allocations
        Args:
            path_to_folder (str): 
                A string indicating the path to the folder where the csv file is to be saved.
        """
        weights = list(range(0, 101, self.increment_decrement))
        generate_portfolios = sorted(product(weights, repeat=len(self.assets)), reverse=True)
        portfolio_allocations = pd.DataFrame([portfolio for portfolio in list(generate_portfolios) if sum(portfolio) == 100], columns=self.assets)

        if os.path.isdir(f"{path_to_folder}") == False: os.mkdir(f"{path_to_folder}")
    
        portfolio_allocations.to_csv(path_or_buf=f"{path_to_folder}/portfolio_allocations.csv", index=False)
        
        
    def treat_csv_files(self, path_to_folder: str):
        
        asset_csv_names = {"ST":"amundi-msci-wrld-ae-c.csv", "CB":"ishares-global-corporate-bond-$.csv", "PB":"db-x-trackers-ii-global-sovereign-5.csv", "GO":"spdr-gold-trust.csv", "CA":"usdollar.csv"}
        remove_keys = [asset for asset in asset_csv_names.keys() if asset not in self.assets]
        for asset in remove_keys: del asset_csv_names[asset] 
        path_csvs_availables = [f"{path_to_folder}/{csv_name}" for _, csv_name in asset_csv_names.items() if os.path.exists(f"{path_to_folder}/{csv_name}")] 
        if len(asset_csv_names) != len(path_csvs_availables): exit("Error, the csv files of the desired assets are not available in the specified path")
        
        csvs_processed = {}
        type_asset_index = 0
        for csv_file in path_csvs_availables:
    
            df = pd.read_csv(csv_file)
            # Date to str
            df["Date"] = pd.to_datetime(df["Date"])
            df["Date"] = df["Date"].dt.date
            df["Date"] = df["Date"].apply(lambda x: str(x))
            # Col name changed and % character deleted
            df = df.rename(columns={"Change %": "Change"})
            df["Change"] = df["Change"].apply(lambda x: x.replace("%", ""))
            # Missing dates
            missing_dates = pd.date_range(start='2020-01-01', end='2020-12-31').difference(df["Date"])
            missing_dates_df = pd.DataFrame(missing_dates.strftime('%Y-%m-%d'), columns=["Date"])
            # For new dates, columns "Price" and "Change" are assigned the average of each column
            avg_price = df["Price"].mean()
            missing_dates_df["Price"] = round(avg_price, 2)
            avg_change = df["Change"].apply(lambda x: pd.to_numeric(x.replace("%", ""))).mean()
            missing_dates_df["Change"] = round(avg_change, 2)

            # If "Vol." column in pd.DataFrame then replace "K" (1e+3), "M" (1e+6) and "-" characters by mean of the column. The missing date rows the same
            if "Vol." in df.columns:
                df = df.rename(columns={"Vol.": "Vol"})
                units_val = {"K":1e+3, "M":1e+6}
                # If "Vol" value is in all rows "-" drop "Vol"
                if df["Vol"].str.contains("-").count() == len(df):
                    df.drop("Vol", inplace=True, axis=1)
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
            complete_dataframe = pd.concat([missing_dates_df, df], ignore_index=True).sort_values(by="Date").reset_index(drop=True)
            csvs_processed[self.assets[type_asset_index]] = tuple(complete_dataframe)
            type_asset_index += 1
            
            
        return csvs_processed




    def generate_portfolio_metrics_csv(self, path_to_folder: str, purchase_date: str, money_invested: float):
        """
        Create portfolio allocations with increment/decrement=20%
        Args:
            path_to_folder (str): 
                A string indicating the path to the folder where the csv file is to be saved.
            money_invested (float):
                A float that indicates the amount of money that SAM want to invest.
        """
        # ST --> Stocks --> amundi-msci-wrld-ae-c.csv|| CB --> Corporate bonds --> ishares-global-corporate-bond-$.csv 
        # PB --> Public bonds --> db-x-trackers-ii-global-sovereign-5.csv || GO --> Gold --> spdr-gold-trust.csv || CA --> Cash --> usdollar.csv 
    
        # Num shares (bj) se calcula con los datos del dia 01,01,2020 ¿¿¿???
    
        # Precio de la accion (pc) es el de los datos del dia 12,31,2020 
        # Num Shares (bj) = dinero destinado a una accion (depende del porcentaje de dinero que se lleve esa accion [esto hay q calcularlo]) / precio de la accion el dia de la compra (pb)
    


if __name__ == "__main__":
    
    
    # increment_decrement = float(input("Please, write the value for the increment/decrement (the project statement recommends either 20 or 0.2, but it could be another one): "))
    # if increment_decrement < 1.0: increment_decrement *= 10
    assets = input("Please, write the assets from which you want to create the portfolio without quotes and separated by spaces ('ST' 'CB' 'PB' 'GO' 'CA'): ")
    # path_to_folder = input("Please, write the route when you want spawn portfolio_allocations.csv files: ")
    print(len(Portfolio(increment_decrement=20, assets=assets).treat_csv_files("part1/csv_files")))
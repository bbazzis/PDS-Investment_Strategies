#!/usr/bin/env python3
from data_generation.data_generation import *
from web_scraping.web_scraping import *


path_to_folder_csv_webscraping = input("Please, write the route when you want spawn web scraping csv files: ")
dataset = input('''Please, write one of the following words (without quotes) that represent the csv to spawn:
                 - "All" --> to create all datasets.
                 - "Stocks" --> to create amundi-msci-wrld-ae-c.csv
                 - "Corporate bonds" --> to create ishares-global-corporate-bond-$.csv
                 - "Public bonds "--> to create db-x-trackers-ii-global-sovereign-5.csv
                 - "Golds to create" --> spdr-gold-trust.csv
                 - "Cash" --> to create usdollar.csv 
                 Enter chosen option: ''')
    
ObtainCSVFilesFromWeb(web_browser='Chrome', web_page='https://www.investing.com/').create_datasets_from_investing(path_to_folder=path_to_folder_csv_webscraping, dataset=dataset)

path_to_folder_portfolio = input("Please, type the route when you want spawn \033[1m portfolio_allocations.csv \033[0m and \033[1m portfolio_metrics.csv \033[0m files: ")
    
increment_decrement = float(input("Please, write the value for \033[1m the increment/decrement (the project statement recommends either 20 or 0.2, but it could be another one): \033[0m "))
if increment_decrement < 1.0: increment_decrement *= 100
increment_decrement = int(increment_decrement)
assets = input("Please, write \033[1m the assets acronyms \033[0m from which you want to create the portfolio without quotes and separated by spaces \033[1m ('ST' 'CB' 'PB' 'GO' 'CA'):\033[0m ")
date = input("Please, write \033[1m the date \033[0m from which you want to generate metrics \033[1m (2020-01-01 recommended by the statement). \033[0m The date must be in the format 'YYYY-MM-DD': ")
    
portfolio = Portfolio(path_to_folder=path_to_folder_portfolio, increment_decrement=increment_decrement, assets=assets) 
portfolio_allocations = portfolio.generate_portfolio_allocations_csv() 
clean_webscraping_csv_files = portfolio.treat_csv_files(path_to_folder=path_to_folder_csv_webscraping) 
    
portfolio.generate_portfolio_metrics_csv(treat_csv_files=clean_webscraping_csv_files, portfolio_allocations=portfolio_allocations, purchase_date=date)
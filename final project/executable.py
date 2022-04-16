#!/usr/bin/env python3
from data_generation.data_generation import *
from web_scraping.web_scraping import *
from data_analysis.data_analysis import *


folder_path_csv_webscraping = input("Please, write the route when you want spawn web scraping csv files: ")
dataset_name = input('''Please, write one of the following words (without quotes) that represent the csv to spawn:
                 - "All" --> to create all csv files.
                 - "Stocks" --> to create amundi-msci-wrld-ae-c.csv
                 - "Corporate bonds" --> to create ishares-global-corporate-bond-$.csv
                 - "Public bonds "--> to create db-x-trackers-ii-global-sovereign-5.csv
                 - "Golds to create" --> spdr-gold-trust.csv
                 - "Cash" --> to create usdollar.csv 
                 Enter chosen option: ''')
    
ObtainCSVFilesFromWeb(web_browser='Chrome', web_page='https://www.investing.com/').create_datasets_from_investing(folder_path=folder_path_csv_webscraping, dataset_name=dataset_name)

path_to_folder_portfolio = input("Please, type the route when you want spawn \033[1m portfolio_allocations.csv \033[0m and \033[1m portfolio_metrics.csv \033[0m files: ")
    
increment_decrement = float(input("Please, write the value for \033[1m the increment/decrement (the project statement recommends either 20 or 0.2, but it could be another one): \033[0m "))
if increment_decrement < 1.0: increment_decrement *= 100
increment_decrement = int(increment_decrement)
assets = input("Please, write \033[1m the assets acronyms \033[0m from which you want to create the portfolio without quotes and separated by spaces \033[1m ('ST' 'CB' 'PB' 'GO' 'CA'):\033[0m ")
date = input("Please, write \033[1m the date \033[0m from which you want to generate metrics \033[1m (2020-01-01 recommended by the statement). \033[0m The date must be in the format 'YYYY-MM-DD': ")
    
portfolio = Portfolio(folder_path=path_to_folder_portfolio, assets=assets, increment_decrement=increment_decrement) 
portfolio_allocations = portfolio.generate_portfolio_allocations_csv() 
clean_webscraping_csv_files = portfolio.treat_csv_files(web_scraping_csv_folder_path=folder_path_csv_webscraping) 
    
portfolio.generate_portfolio_metrics_csv(treat_csv_files=clean_webscraping_csv_files, portfolio_allocations=portfolio_allocations, purchase_date=date)

consent = input("Do you want to spawn graphs from portfolio_metrics.csv? \033[1m(Yes/No)\033[0m: ")
if consent == "Yes":
    save_graph_folder = input("Please write the route when you want spawn the graphs: ")
    graphs = CreateGraphsFromCsv(path_to_csv_file=path_to_folder_portfolio + "/portfolio_metrics.csv", folder_to_save_graphs=save_graph_folder)
    graphs.bar_plot_type_portfolio()
    graphs.bar_plot_sum_assets()
    graphs.scatter_chart("VOLAT", "RETURN", "COLOR", "Risk-Return bubble chart")             
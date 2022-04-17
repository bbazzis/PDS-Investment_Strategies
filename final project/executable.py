#!/usr/bin/env python3
"""
This file allow the user to execute all .py files more comfortably.
Please, execute this file with the command: python3 executable.py
"""
from data_generation.data_generation import *
from web_scraping.web_scraping import *
from data_analysis.data_analysis import *

class color:
    PURPLE, BOLD, END = '\033[95m', '\033[1m', '\033[0m'
   
folder_path_csv_webscraping = input("Please, write the" + color.PURPLE + color.BOLD + " route" + color.END + " when you want" + color.PURPLE + color.BOLD + " spawn web scraping csv files: " + color.END)
dataset_name = input('''Please,''' + color.PURPLE + color.BOLD + ''' write one of the following words (without quotes)\033[0m that represent the csv to spawn:
                 - "''' + color.PURPLE + color.BOLD + '''All''' + color.END + '''" --> to create''' + color.PURPLE + color.BOLD + ''' all csv files.''' + color.END + '''
                 - "''' + color.PURPLE + color.BOLD + '''Stocks''' + color.END + '''" --> to''' + color.PURPLE + color.BOLD + ''' create amundi-msci-wrld-ae-c.csv''' + color.END + '''
                 - "''' + color.PURPLE + color.BOLD + '''Corporate bonds''' + color.END + '''" --> to create''' + color.PURPLE + color.BOLD + ''' mishares-global-corporate-bond-$.csv''' + color.END + '''
                 - "''' + color.PURPLE + color.BOLD + '''Public bonds''' + color.END + '''"--> to create''' + color.PURPLE + color.BOLD + ''' db-x-trackers-ii-global-sovereign-5.csv''' + color.END + '''
                 - "''' + color.PURPLE + color.BOLD + '''Golds''' + color.END + '''" --> to create''' + color.PURPLE + color.BOLD + ''' spdr-gold-trust.csv''' + color.END + '''
                 - "''' + color.PURPLE + color.BOLD + '''Cash''' + color.END + '''" --> to create''' + color.PURPLE + color.BOLD + ''' usdollar.csv''' + color.END + '''
                 Enter chosen option: ''')
    
ObtainCSVFilesFromWeb(web_browser='Chrome', web_page='https://www.investing.com/').create_datasets_from_investing(folder_path=folder_path_csv_webscraping, dataset_name=dataset_name)

path_to_folder_portfolio = input("Please, type the" + color.PURPLE + color.BOLD + " route" + color.END + " when you want spawn" + color.PURPLE + color.BOLD + " portfolio_allocations.csv and portfolio_metrics.csv" + color.END + " files: ")
    
increment_decrement = float(input("Please, write the value for the" + color.PURPLE + color.BOLD + " increment/decrement" + color.END + " (the project" + color.PURPLE + color.BOLD + " statement recommends either 20 or 0.2, but it could be another one): " + color.END))
if increment_decrement < 1.0: increment_decrement *= 100
increment_decrement = int(increment_decrement)
assets = input("Please, write the assets acronyms from which you want to create the portfolio without quotes and separated by spaces (" + color.PURPLE + color.BOLD + " ST CB PB GO CA" + color.END + " ): ")
date = input("Please, write the date from which you want to generate metrics (" + color.PURPLE + color.BOLD + " 2020-01-01 recommended by the statement" + color.END + " but it could be another one). The date must be in the format" + color.PURPLE + color.BOLD + " YYYY-MM-DD" + color.END + ": ")
    
portfolio = Portfolio(folder_path=path_to_folder_portfolio, assets=assets, increment_decrement=increment_decrement) 
portfolio_allocations = portfolio.generate_portfolio_allocations_csv() 
clean_webscraping_csv_files = portfolio.treat_csv_files(web_scraping_csv_folder_path=folder_path_csv_webscraping) 
    
portfolio.generate_portfolio_metrics_csv(treat_csv_files=clean_webscraping_csv_files, portfolio_allocations=portfolio_allocations, purchase_date=date)

consent = input("Do you want to spawn graphs from portfolio_metrics.csv? (" + color.PURPLE + color.BOLD + "Yes/No" + color.END + "): ")
if consent == "Yes":
    save_graph_folder = input("Please, write the" + color.PURPLE + color.BOLD + " route" + color.END + " when you want" + color.PURPLE + color.BOLD + " spawn the graphs" + color.END + ": ")
    graphs = CreateGraphsFromCsv(path_to_csv_file=path_to_folder_portfolio + "/portfolio_metrics.csv", folder_to_save_graphs=save_graph_folder)
    graphs.bar_plot_type_portfolio()
    graphs.bar_plot_investing_asset()
    graphs.bar_plot_sum_assets()
    graphs.scatter_chart()             
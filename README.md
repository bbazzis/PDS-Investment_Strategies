# PDS-Investment_Strategies
Assigment for Programming for Data Science subject

To run the code (```final_project version folder```) type in terminal the following lines:

```console
python3 executable.py
```
once executed follow the instructions that appears on the console.


### Example of values given to console instructions:

Please, write the ```route``` when you want ```spawn web scraping csv files```: 
```console 
web_scraping_csv_files_folder
```
Please, write one of the following words (without quotes) that represent the csv to spawn:\
                 - ```All``` --> to create all datasets.\
                 - ```Stocks``` --> to create ```amundi-msci-wrld-ae-c.csv```\
                 - ```Corporate bonds``` --> to create ```ishares-global-corporate-bond-$.csv```\
                 - ```Public bonds``` --> to create ```db-x-trackers-ii-global-sovereign-5.csv```\
                 - ```Golds``` --> to create ```spdr-gold-trust.csv```\
                 - ```Cash``` --> to create ```usdollar.csv```\
                 Enter chosen option: 
```console 
All
```
Please, type the ```route``` when you want ```spawn portfolio_allocations.csv and portfolio_metrics.csv```  files: 
```console 
portfolios_csv_files_folder
```
Please, write the value for  the increment/decrement (the project ```statement recommends either 20 or 0.2```, but it could be another one): 
```console 
20
```
Please, write  the assets acronyms  from which you want to create the portfolio without quotes and separated by spaces  (```ST``` ```CB``` ```PB``` ```GO``` ```CA```): 
```console 
ST CB PB GO CA
```
Please, write  the date  from which you want to generate metrics  (```2020-01-01 recommended by the statement``` but it could be another one).  The date must be in the format ```YYYY-MM-DD```: 
```console 
2020-01-01
```
Do you want to spawn graphs from portfolio_metrics.csv? (```Yes```/```No```): 
```console 
Yes
```
Please write the ```route``` when you want ```spawn the graphs```: 
```console 
graphs_folder
```

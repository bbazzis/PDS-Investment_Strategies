#!/usr/bin/env python3
"""
This file contains all the code implementation corresponding to the part 2.1 of the project.
The code below, generate some graphs based on portfolio_metrics.csv, created by data_generation.py.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np


class CreateGraphsFromCsv():
    """
    This class allows to spawn the graphs.
    """
    def __init__(self, path_to_csv_file: str, folder_to_save_graphs: str):
        """
        Init CreateGraphsFromCsv.
        
        Args:
            path_to_csv_file (str): 
                A string indicating the path to portfolio_metrics.csv.
            folder_to_save_graphs (str):
                A string that indicates the folder where you want to save the graphs.
        """
        
        # Parameter checking.
        try:
            assert os.path.isfile(path_to_csv_file), f"\033[1m ERROR: \033[0m The path to the csv file ({path_to_csv_file}) is not valid."
            assert "portfolio_metrics.csv" in path_to_csv_file, "\033[1m ERROR: \033[0m The file is not a portfolio_metrics.csv file. Please, check the path."
        except AssertionError as error:
            print(error)
            exit(1)
        if os.path.isdir(folder_to_save_graphs) == False: os.mkdir(folder_to_save_graphs)
        self.folder_to_save_graphs = folder_to_save_graphs
        self.path_to_csv_file = path_to_csv_file
        
        
    def bar_plot_type_portfolio(self, title="Number of each portfolio", x_label=None, y_label="Number of Portfolios", save_graph=True):
        """
        Create a bar plot which indicates the number of portfolios of each type (positive, negative or neutral return).
        
        Args:
            title (str): 
                A string indicating the title for the bar plot.
            x_label (str): 
                A string indicating the label for x-axe.
            y_label (str): 
                A string indicating the label for y-axe.
            save_graph (bool): 
                A boolean indicating if the user want to save the graph.
        """
        
        df = pd.read_csv(self.path_to_csv_file)
        
        bars = ["Positive Portfolio", "Neutral Portfolio", "Negative Portfolio"]
        data = [len(df[df["RETURN"] > 0]), len(df[df["RETURN"] == 0]), len(df[df["RETURN"] < 0])]
        df = pd.DataFrame(data, bars, columns=["Number of Portfolios"])
        sns.set(style="darkgrid")
        sns.barplot(x=list(df.index), y=list(df["Number of Portfolios"]), palette=["green", "blue", "red"])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if save_graph: plt.savefig(self.folder_to_save_graphs + "/bar_plot.png")
        plt.show()
        
    
    def bar_plot_sum_assets(self, title="Average percentage of investments for each type of portfolio since 2020-01-01 to 2020-12-31", y_label="Average investment percentage", save_graph=True):
        """
        Create a bar plot of the sum of investments in each asset for each type of portfolio (Positive, negative or neutral return).
        
        Args:
            title (str): 
                A string indicating the title for the bar plot.
            y_label (str): 
                A string indicating the label for y-axe.
            save_graph (bool): 
                A boolean indicating if the user want to save the graph.
        """

        df = pd.read_csv(self.path_to_csv_file)
        df["TYPE_PORTFOLIO"] = ["Positive portfolio" if x > 0 else "Negative portfolio" if x < 0 else "Neutral portfolio" for x in df["RETURN"]]
        labels = list(np.unique(df["TYPE_PORTFOLIO"]))
        name_assets = [name for name in list(df.columns) if name in ["ST", "CB", "PB", "GO", "CA"]]
        asset_sum_percentage = {}

        for name in name_assets:
            asset_sum_percentage[name] = [df[df["RETURN"] < 0][name].mean(), df[df["RETURN"] == 0][name].mean(), df[df["RETURN"] > 0][name].mean()]

        barWidth = 0.1

        r1 = np.arange(3) 
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]
        r4 = [x + barWidth for x in r3]
        r5 = [x + barWidth for x in r4]

        plt.subplots(figsize=(8,8))

        for k, v in asset_sum_percentage.items():
            if k == "ST":
                plt.bar(r1, v, color="blue", width=barWidth, edgecolor="white", label='Stocks')
            elif k == "CB":
                plt.bar(r2, v, color="red", width=barWidth, edgecolor="white", label='Corporate Bonds')
            elif k == "PB":
                plt.bar(r3, v, color="green", width=barWidth, edgecolor="white", label='Public Bonds')
            elif k == "GO":
                plt.bar(r4, v, color="yellow", width=barWidth, edgecolor="white", label='Gold')
            elif k == "CA":   
                plt.bar(r5, v, color="purple", width=barWidth, edgecolor="white", label='Cash')

        plt.ylabel(y_label)
        plt.xticks(np.arange(3)+barWidth+0.1, labels)
        plt.title(title)
        plt.legend()
        if save_graph: plt.savefig(self.folder_to_save_graphs + "/bar_plot_sum_assets.png")
        plt.show()
        
        
    def bar_plot_investing_asset(self, title="Average return investing in ", x_label="Percentage of investement", y_label="Average return", save_graph=True):
        """
        Create one bar plot for each asset and each one show the return per percentage invested in that asset.
        
        Args:
            title (str): 
                A string indicating the title for the bar plot.
            x_label (str): 
                A string indicating the label for x-axe.
            y_label (str): 
                A string indicating the label for y-axe.
            save_graph (bool): 
                A boolean indicating if the user want to save the graph.
        """
        df = pd.read_csv(self.path_to_csv_file)
        name_assets = [name for name in list(df.columns) if name in ["ST", "CB", "PB", "GO", "CA"]]
    
        fig, ax = plt.subplots(5, 1, figsize=(10, 20))
        idx = 0
        for name in name_assets:
            df2 = df[[name, "RETURN"]]
            df2 = df2.groupby(name).mean().sort_values(name)
            
            sns.set(style="darkgrid")
            sns.barplot(ax=ax[idx], x=list(df2.index), y=list(df2["RETURN"]), palette=["green", "blue", "red", "yellow", "orange", "purple"])
            ax[idx].set_xlabel(x_label)
            ax[idx].set_ylabel(y_label)
            ax[idx].set_title(title + name)
            idx += 1
        
        fig.tight_layout()   
        if save_graph: plt.savefig(self.folder_to_save_graphs + "/average_return_investing_asset.png")    
        plt.show()
        
            
    def scatter_chart(self, x="VOLAT", y="RETURN", color="COLOR", title="Risk-Return bubble chart", x_label="Risk (Volatility)", y_label="Return", save_graph=True):
        """
        Create a scatter chart from csv specified in the constructor of the class .
        
        Args:
            x (list):
                A list of values for x-axe.
            y (list):
                A list of values for y-axe.
            color (list):
                A list of values for color.
            title (str): 
                A string indicating the title for the bar plot.
            x_label (str): 
                A string indicating the label for x-axe.
            y_label (str): 
                A string indicating the label for y-axe.
            save_graph (bool): 
                A boolean indicating if the user want to save the graph.
        """
        
        df = pd.read_csv(self.path_to_csv_file)
        df["COLOR"] = ["green" if x > 0 else "red" if x < 0 else "blue" for x in df["RETURN"]]
        df["TYPE_PORTFOLIO"] = ["Positive portfolio" if x > 0 else "Negative portfolio" if x < 0 else "Neutral portfolio" for x in df["RETURN"]]

        plt.subplots(figsize=(8,8))
        plt.scatter(x = df[df["RETURN"] > 0][x], s=100, y = df[df["RETURN"] > 0][y], c=df[df["RETURN"] > 0][color], cmap="Accent", alpha=0.6, edgecolors="white", linewidth=2 , label="Positive Portfolio")
        plt.scatter(x = df[df["RETURN"] == 0][x], s=100, y = df[df["RETURN"] == 0][y], c=df[df["RETURN"] == 0][color], cmap="Accent", alpha=0.6, edgecolors="white", linewidth=2, label="Neutral Portfolio")
        plt.scatter(x = df[df["RETURN"] < 0][x], s=100, y = df[df["RETURN"] < 0][y], c=df[df["RETURN"] < 0][color], cmap="Accent", alpha=0.6, edgecolors="white", linewidth=2, label="Negative Portfolio")
        plt.legend()
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if save_graph: plt.savefig(self.folder_to_save_graphs + "/scatter_chart.png")
        plt.show()  
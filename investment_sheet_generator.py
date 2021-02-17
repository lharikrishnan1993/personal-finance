import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import pandas as pd

import investment_chart_generator

class InvestmentSheetGenerator:
    def __init__(self, df, title):
        self.df = df
        self.title = title
        self.items = []
        self.clean_data()
        self.cg = investment_chart_generator.InvestmentChartGenerator(self.df)
        self.main()

    def clean_data(self):
        # self.df = self.df[self.df.Sector != 'Total Market']
        self.df = self.df[(self.df['Transaction Type'] == 'BUY') | (self.df['Transaction Type'] == 'SELL')]

    def main(self):
        heading = html.H1(self.title, style={'textAlign':'center'})
        self.items.append(heading)
        self.piecharts()
        self.linecharts()

    def piecharts(self):
        piechart = dbc.Card(
            [dcc.Graph(id='pie-chart', figure=go.Figure(self.cg.pie('$')))], 
            body=True,
        )
        self.items.append(piechart)

    def linecharts(self):
        linechart = dbc.Card(
            [dcc.Graph(id='line-chart', figure=self.cg.generate_comparison_plot())], 
            body=True,
        )
        self.items.append(linechart)

    def getSheet(self):
        return self.items
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import pandas as pd

import expense_chart_generator

class ExpenseSheetGenerator:
	def __init__(self, df, title, category, currency, currency_symbol):
		self.df = df
		self.title = title
		self.items = []
		self.cg = expense_chart_generator.ExpenseChartGenerator(df, category)
		self.currency = currency
		self.currency_symbol = currency_symbol
		self.main()

	def main(self):
		heading = html.H1(self.title,
                          style={'textAlign':'center'})
		self.items.append(heading)
		self.items.append(html.H4('', className="card-title", style={'padding':20}))
		self.piecharts()
		self.items.append(html.H4('', className="card-title", style={'padding':20}))		
		self.barcharts()

	def piecharts(self):
		piechart = dbc.Card(
		    [  
		        dcc.Graph(id='pie-chart', 
		        		  figure=go.Figure(self.cg.pie(self.currency, self.currency_symbol)))
		    ], 
		    body=True,
		)
		self.items.append(piechart)

	def barcharts(self):
		self.items = self.items + self.cg.bar(self.currency, self.currency_symbol)

	def getSheet(self):
		return self.items
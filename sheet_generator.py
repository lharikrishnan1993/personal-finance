import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import pandas as pd

import chart_generator

class SheetGenerator:
	def __init__(self, df, title, category):
		self.df = df
		self.title = title
		self.items = []
		self.cg = chart_generator.ChartGenerator(df, category)
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
		        		  figure=go.Figure(self.cg.pie('INR')))
		    ], 
		    body=True,
		    # style={'height':'80vh'}
		)
		self.items.append(piechart)

	def barcharts(self):
		self.items = self.items + self.cg.bar('INR')

	def getSheet(self):
		return self.items
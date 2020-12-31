import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import pandas as pd

import chart_generator

class SheetGenerator:
	def __init__(self, df, title, category, selector, show_pie=False, show_bar=True):
		self.df = df
		self.title = title
		self.items = []
		self.cg = chart_generator.ChartGenerator(df, category, selector)
		self.show_pie = show_pie
		self.show_bar = show_bar
		self.main()

	def main(self):
		heading = html.H1(self.title,
                          style={'textAlign':'center'})
		self.items.append(heading)
		if self.show_pie: 
			self.piecharts()
		if self.show_bar:
			self.barcharts()

	def piecharts(self):
		piechart = dcc.Graph(id='pie-chart',
                  		     figure=go.Figure(self.cg.pie()))
		self.items.append(piechart)

	def barcharts(self):
		# barchart = dcc.Graph(id='bargraph',dren property of a component 
  #                 		     figure=go.Figure(self.cg.bar()))
		self.items = self.items + self.cg.bar()

	def getSheet(self):
		return self.items
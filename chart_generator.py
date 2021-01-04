import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd

class ChartGenerator:
	def __init__(self, df, category):
		self.df = df
		self.category = category

	def generate_pie(self, labels, values, start, end, sym='₹'):
		return go.Pie( labels=labels, 
			           values=values, 
			           texttemplate="%{label}<br>%{percent}",
			           domain=dict(x=[start, end]),
			           textposition="inside",
			           insidetextorientation='radial',
			           direction="counterclockwise",
			           hovertemplate="Category: %{label}<br>"
			           				 + sym + "%{value:,.2f}<br>"
			           				 "%{percent}<extra></extra>")

	def generate_bar(self, labels, values, df_category, sym='₹'):
		Bar = go.Figure(
				go.Bar( 
					x=labels, 
		            y=values,
		            hovertext="Name: " + 
		                      df_category.Name + 
		                      "<br>Payment Mode: " + 
		                      df_category['Payment Mode'] + 
		                      "<br>Comments: " + 
		                      df_category.Comments,
		            hovertemplate="Date: %{x}<br>"
		           				 "Amount: " + sym + "%{y} <br>"
		           				 "%{hovertext}<extra></extra>",
		            hoverinfo="skip", 
		            showlegend=False))
		Bar.update_layout(bargap=0.5)
		Bar.update_xaxes(tickformat="%b %e, %Y", tickangle=45, dtick='0')
		return Bar

	def pie(self):
		fig_pie = make_subplots(
	        rows=1, 
	        cols=2, 
	        column_widths=[0.5, 0.5], 
	        subplot_titles=("INR", "USD"), 
	        specs=[[{"type": "domain"}, 
	                {"type": "domain"}]], 
	        horizontal_spacing=0.25)

		fig_pie.add_trace(
			self.generate_pie(self.df[self.category], 
							  self.df['INR'], 0, 0.5, '₹'), 1, 1)
		fig_pie.add_trace(
			self.generate_pie(self.df[self.category], 
							  self.df['USD'], 0.5, 1.0, '$'), 1, 2)	

		fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))

		return fig_pie

	def bar(self, currency):
		graphs = []
		for selector in self.df[self.category].unique():
			if selector == 'Artificial':
				continue

			df_category = self.df[self.df[self.category].eq(selector) | 
								  self.df[self.category].eq('Artificial')]

			fig_bar=self.generate_bar(df_category.Date, 
								  	  df_category[currency], 
								  	  df_category)	

			graphs.append(
				dbc.Card(
		    	[  
			    	html.H4(selector, className="card-title", 
			    					  style={'textAlign':'center'}),
			    	html.H6(df_category['Date'].tolist()[0].month_name() + 
			    			' ' + 
			    			str(df_category['Date'].tolist()[0].year), 
			    			className="card-subtitle", 
			    			style={'textAlign':'center'}),

					dcc.Graph(id='bargraph', figure=go.Figure(fig_bar)),
				], body=True)
				)
			graphs.append(html.H4('', className="card-title", style={'padding':20}))

		return graphs
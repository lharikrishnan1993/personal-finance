import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

import price_loader as pl
import spy_investments as spy

import pandas as pd

class InvestmentChartGenerator:
    def __init__(self, df):
        self.df = df
        self.price_loader = pl.PriceLoader('2019-10-23', '1d')
        self.comparison_data = None
        self.get_comparison_data()
        self.base_investment = spy.BaseStockInvestmentCalculator(self.comparison_data, self.df)

    def get_comparison_data(self):
        try:
            self.comparison_data = self.price_loader.getData('SPY')
        except:
            print('Personal-Finance -> Error in downloading Comparison Data from Yahoo Finance')

    def generate_line(self, df, x, y, title):
        Line = go.Figure(px.area(df, x=x, y=y, title=title))
        lowest_point = y.min() * 0.98
        highest_point = y.max() * 1.02        
        Line.update_layout(
            yaxis=dict(range=[lowest_point, highest_point])
            )
        return Line

    def generate_comparison_plot(self):
        return self.generate_line(self.comparison_data, 
                                  x=self.comparison_data['Date'], 
                                  y=self.comparison_data['Close'], 
                                  title='SPY')

    def generate_pie(self, labels, values, sym='₹'):
        Pie = go.Figure(
				go.Pie( 
					labels=labels, 
		            values=values,
                    texttemplate="%{label}<br>%{percent}",
                    textposition='inside',
		            insidetextorientation='radial',
		            direction="counterclockwise",
		            hovertemplate="Category: %{label}<br>"
		           				+ sym + "%{value:,.2f}<br>"
		           				"%{percent}<extra></extra>"))
                                   
        Pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), legend=dict(
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=0.99
        ))
        
        return Pie
        
    def generate_bar(self, labels, values, df_category, sym='₹'):
        Bar = go.Figure(
				go.Bar( 
					x=labels, 
		            y=values,
		            hovertext="Name: " + 
		                      df_category.Name + 
		                      "<br>Payment Mode: " + 
		                      df_category['Payment Mode'] + 
		                      "<br>Tags: " + 
		                      df_category.Tags,
		            hovertemplate="Date: %{x}<br>"
		           				 "Amount: " + sym + "%{y} <br>"
		           				 "%{hovertext}<extra></extra>",
		            hoverinfo="skip", 
		            showlegend=False), 
				)
        Bar.update_layout(bargap=0.5)
        Bar.update_xaxes(tickformat="%b %e, %Y", tickangle=45, dtick='0')
        return Bar
        
    def pie(self, currency_symbol='₹'):
        return self.generate_pie(self.df['Sector'], self.df['Amount'], currency_symbol)
    
    def bar(self, currency, currency_symbol='₹'):
        graphs = []
        for selector in self.df[self.category].unique():
            if selector == 'Artificial':
                continue
                
            df_category = self.df[self.df[self.category].eq(selector) | 
								  self.df[self.category].eq('Artificial')]
                                  
            fig_bar=self.generate_bar(df_category.Date, 
								  	  df_category[currency], 
								  	  df_category, currency_symbol)	
            
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
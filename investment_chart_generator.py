import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

import price_loader as pl
import spy_investments as spy

from datetime import datetime

import pandas as pd

def format_date_from_current_investments(date):
    return datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')

def format_date_from_base_stock(date):
    return datetime.strptime(str(date), '%Y-%m-%d').strftime('%Y-%m-%d')

class InvestmentChartGenerator:
    def __init__(self, df):
        self.df = df
        self.base_stock = 'VOO'
        self.price_loader = pl.PriceLoader('2019-10-23', '30m')
        self.comparison_data = None
        self.get_comparison_data()
        self.base_investment = spy.BaseStockInvestmentCalculator(self.comparison_data, self.df)
        self.investment_history = pd.DataFrame()

    def get_comparison_data(self):
        try:
            self.comparison_data = self.price_loader.getData(self.base_stock)
            self.comparison_data['Date'] = self.comparison_data['Date'].apply(format_date_from_base_stock)
        except:
            print('Personal-Finance -> Error in downloading Comparison Data from Yahoo Finance')

    def generate_line(self, df, x, y, title,):
        Line = go.Figure(px.area(df, x=x, y=y, title=title))
        lowest_point = y.min() * 0.98
        highest_point = y.max() * 1.02        
        Line.update_layout(
            yaxis=dict(range=[lowest_point, highest_point])
            )
        return Line

    def generate_base_stock_plot(self):
        self.comparison_data = self.base_investment.getBaseInvestmentHoldings()
        purchase_price = self.comparison_data['Weighted Average Price'] * self.comparison_data['Shares Available']
        equity_close = self.comparison_data['Equity Close']
        equity_low = self.comparison_data['Equity Low']
        equity_high = self.comparison_data['Equity High']               
        equity_purchase_amount = self.comparison_data.tail(1)['Invested Amount'].values[0]

        fig = go.Figure([
            go.Scatter(
                name='Daily Close',
                x=self.comparison_data['Date'],
                y=equity_purchase_amount + equity_close - purchase_price,
                mode='lines',
                line=dict(color='rgb(102, 166, 30)'),
            ),
            go.Scatter(
                name='Daily High',
                x=self.comparison_data['Date'],
                y=equity_purchase_amount + equity_high - purchase_price,
                mode='lines',
                marker=dict(color='rgba(166, 216, 84, 0.5)'),
                line=dict(width=0),
                showlegend=False
            ),
            go.Scatter(
                name='Daily Low',
                x=self.comparison_data['Date'],
                y=equity_purchase_amount + equity_low - purchase_price,
                marker=dict(color='rgba(166, 216, 84, 0.5)'),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(166, 216, 84, 0.5)',
                fill='tonexty',
                showlegend=False
            )
        ])

        fig.update_layout(
            yaxis_title='Invested Amount',
            # title=self.base_stock,
            hovermode="x"
        )

        return fig

    def generate_current_investment_plot(self):
        base_stock_plot = self.generate_base_stock_plot()
        self.comparison_data = self.base_investment.getBaseInvestmentHoldings()        
        purchase_price = self.comparison_data['Weighted Average Price'] * self.comparison_data['Shares Available']
        equity_close = self.comparison_data['Equity Close']
        equity_low = self.comparison_data['Equity Low']
        equity_high = self.comparison_data['Equity High']               
        equity_purchase_amount = self.comparison_data.tail(1)['Invested Amount'].values[0]

        self.df['Date'] = self.df['Date'].apply(format_date_from_current_investments)
        stocks_held = self.df['Ticker Tag'].unique()

        for stock in stocks_held:
            success, stock_file_name = self.price_loader.storeData(stock)
            if success == False:
                print('Error fetching data for ' + stock)
                continue

        self.investment_history['Date'] = self.comparison_data['Date']

        for stock in stocks_held:
            profit_per_stock = []
            for index, row in self.comparison_data.iterrows():
                date = row.Date
                if datetime.strptime(date, '%Y-%m-%d') < datetime.strptime(self.df[self.df['Ticker Tag'] == stock].Date.iloc[0], '%Y-%m-%d'):
                    profit_per_stock.append(0.0)
                    continue
                stock_data = pd.read_csv('Stock Information/' + stock + '.csv')
                df_date = self.df[self.df['Date'] <= date]
                df_company = df_date[df_date['Ticker Tag'] == stock]
                stock_close_price = stock_data[stock_data['Date'] == date].Close.values
                if len(stock_close_price) > 0:
                    stock_close_price = stock_close_price[0]
                else:
                    profit_per_stock.append(0.0)
                    continue
                if df_company.Quantity.sum() <= 1e-5:
                    profit_per_stock.append(0.0)
                else:
                    profit_per_stock.append(stock_close_price * df_company.Quantity.sum() - df_company.Amount.sum())
            self.investment_history[stock] = profit_per_stock
        
        self.investment_history['Return'] = self.investment_history.sum(axis=1)
        self.investment_history['Return'] += self.df.Amount.sum()

        return go.Scatter(x=self.investment_history['Date'], 
                                     y=self.investment_history['Return'], name='Current Investments')

    def generate_comparison_plot(self):        
        base_stock_plot = self.generate_base_stock_plot()
        self.comparison_data = self.base_investment.getBaseInvestmentHoldings()
        purchase_price = self.comparison_data['Weighted Average Price'] * self.comparison_data['Shares Available']
        equity_close = self.comparison_data['Equity Close']
        equity_low = self.comparison_data['Equity Low']
        equity_high = self.comparison_data['Equity High']               
        equity_purchase_amount = self.comparison_data.tail(1)['Invested Amount'].values[0]

        base_stock_plot.add_trace(self.generate_current_investment_plot())

        return base_stock_plot

    def generate_pie(self, labels, values, sym='₹'):
        Pie = go.Figure(
				go.Pie( 
					labels=labels, 
		            values=values,
                    hole=0.4,
                    texttemplate="%{label}<br>%{percent}",
                    textposition='inside',
		            insidetextorientation='radial',
		            # direction="counterclockwise",
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
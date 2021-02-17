'''
Goal of this file is to figure out what will be the status
of funds if the investments had been made on the same day to 
SPY (BaseStock) instead of the investments made into p=handpicked stocks
'''

import pandas as pd
from datetime import datetime

def format_date(date):
    return datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')

class BaseStockInvestmentCalculator:
    def __init__(self, base_stock, current_investments):
        self.base_stock = base_stock
        self.current_investments = current_investments
        self.trading_days = []
        self.net_trades = pd.DataFrame([])
        self.main()

    def identify_trading_days(self):
        self.trading_days = self.current_investments['Date'].unique()

    def calculate_net_transaction_amount(self, date):
        self.net_trades = self.net_trades.append({'Date': date, 
                            'Amount': self.current_investments[self.current_investments['Date'] == date].Amount.sum()}, 
                            ignore_index=True)
    
    def accumulate_shares_in_base_stock(self):
        self.net_trades['Date'] = self.net_trades['Date'].apply(format_date)
        for index, row in self.net_trades.iterrows():
            price = self.base_stock[self.base_stock['Date'] == row['Date']]['Close'].values[0]
            amount = row['Amount']
            shares = amount/price
            date = row['Date']
            self.net_trades.loc[index, 'Shares'] = shares
            self.net_trades.loc[index, 'Price Close'] = price
        
    def calculate_equity_holdings(self):
        last_shares = 0.0
        average_buy_price = 0.0
        invested_amount = 0.0
        for index, row in self.base_stock.iterrows():
            date = datetime.strptime(str(row['Date']), '%Y-%m-%d 00:00:00').strftime('%Y-%m-%d')
            share_availability = self.net_trades[self.net_trades['Date'] == date].Shares.values
            price = self.net_trades[self.net_trades['Date'] == date]['Price Close'].values
            if (len(share_availability) > 0):
                old_last_shares = last_shares
                last_shares += share_availability[0]
                average_buy_price = (average_buy_price * old_last_shares + price[0] * share_availability[0])/last_shares
                invested_amount += price[0] * share_availability[0]
            self.base_stock.loc[index, 'Shares Available'] = last_shares
            self.base_stock.loc[index, 'Equity Close'] = last_shares * row['Close']
            self.base_stock.loc[index, 'Equity High'] = last_shares * row['High']            
            self.base_stock.loc[index, 'Equity Low'] = last_shares * row['Low']                        
            self.base_stock.loc[index, 'Weighted Average Price'] = average_buy_price
            self.base_stock.loc[index, 'Invested Amount'] = invested_amount

    def main(self):
        self.identify_trading_days()
        for date in self.trading_days:
            self.calculate_net_transaction_amount(date)
        self.accumulate_shares_in_base_stock()
        self.calculate_equity_holdings()
         
    def getBaseInvestmentHoldings(self):
        return self.base_stock
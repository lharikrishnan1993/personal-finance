import yfinance as yf
from datetime import datetime
from datetime import date
from datetime import timedelta
import pandas as pd
from os import path

"""
Make this smart enough to read the data available offline and 
check if the latest information is available or not; if available, 
return as df and if not, download store the data (if requested so 
by the user) and return the df. 
"""

def format_date(date):
    if '00:00:00' in str(date):
        return datetime.strptime(str(date), '%Y-%m-%d 00:00:00').strftime('%Y-%m-%d')
    else:
        return str(date)

class PriceLoader:
    def __init__(self, start_date, interval):
        self.interval = interval
        self.start_date = start_date
        self.end_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    def getData(self, ticker):
        try:
            filename  = 'Stock Information/' + ticker + '.csv'
            file_exists = path.exists(filename)
            if not file_exists:                
                df = yf.download(ticker, self.start_date, self.end_date, self.interval, progress=False, prepost=True)
                df = df.reset_index()
                df['Date'] = df['Date'].apply(format_date)
                df.to_csv(filename, index=False)
            else:
                df = pd.read_csv(filename)
                df['Date'] = df['Date'].apply(format_date)
                if df['Date'].iloc[0] != self.start_date or df['Date'].iloc[-1] != self.end_date:
                    last_date = format_date(datetime.strptime(df['Date'].iloc[-1], '%Y-%m-%d') + timedelta(days=2))
                    new_df = yf.download(ticker, last_date, self.end_date, self.interval, progress=False, prepost=True)
                    if new_df.shape[0] > 0:
                        new_df = new_df.reset_index()
                        df = df.append(new_df)
                        df.to_csv(filename, index=False)
            return df
        except:
            print('Error in downloading ' + ticker)

    def storeData(self, ticker):
        try:
            filename = 'Stock Information/' + ticker + '.csv'
            file_exists = path.exists(filename)
            if not file_exists:
                df = yf.download(ticker, self.start_date, self.end_date, self.interval, progress=False, prepost=True)
                df = df.reset_index()
                df['Date'] = df['Date'].apply(format_date)                
                df.to_csv(filename, index=False)
            else:
                df = pd.read_csv(filename)
                df['Date'] = df['Date'].apply(format_date)
                if df['Date'].iloc[0] != self.start_date or df['Date'].iloc[-1] != self.end_date:
                    last_date = format_date(datetime.strptime(df['Date'].iloc[-1], '%Y-%m-%d') + timedelta(days=2))
                    new_df = yf.download(ticker, last_date, self.end_date, self.interval, progress=False, prepost=True)
                    if new_df.shape[0] > 0:
                        new_df = new_df.reset_index()
                        df = df.append(new_df)
                        df.to_csv(filename, index=False)
            return True, filename
        except:
            return False, None
import yfinance as yf
from datetime import datetime

"""
Make this smart enough to read the data available offline and 
check if the latest information is available or not; if available, 
return as df and if not, download store the data (if requested so 
by the user) and return the df. 
"""

class PriceLoader:
    def __init__(self, start_date, interval):
        self.interval = interval
        self.start_date = start_date
        self.end_date = datetime.today().strftime('%Y-%m-%d')

    def getData(self, ticker):
        df = yf.download(ticker, self.start_date, self.end_date, self.interval)
        df = df.reset_index()
        return df
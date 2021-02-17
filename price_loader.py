import yfinance as yf

"""
Make this smart enough to read the data available offline and 
check if the latest information is available or not; if available, 
return as df and if not, download store the data (if requested so 
by the user) and return the df. 
"""

class PriceLoader:
    def __init__(self):
        self.interval = '1d'

    def getData(self, ticker, start, end, interval):
        df = yf.download(ticker, start, end, interval)
        df = df.reset_index()
        return df
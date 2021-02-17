import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def clear_non_transactions(df):
    df = df.loc[df['Transaction Type'] != 'ACH']
    df = df.loc[df['Transaction Type'] != 'CDIV']    
    df = df.loc[df['Transaction Type'] != 'CGAP']
    df = df.loc[df['Transaction Type'] != 'SGAP']
    return df

def view_amount_in_sector(df, sector):
    if sector == 'nan' or sector == 'ETF' or sector == 'null':
        return
    df = df.loc[df['Sector'] == sector]
    return df.Amount.sum()

def categorise_by_sector(df):
    sectors = df.Sector.unique()
    data = {}
    for sector in sectors:
        amount = view_amount_in_sector(df, sector)
        data[sector] = amount
    return data

if __name__ == "__main__":
    df = pd.read_csv('Investments/Robinhood.csv')
    df = clear_non_transactions(df)
    df = df[(df['Transaction Type'] == 'BUY') | (df['Transaction Type'] == 'SELL')] 
    sector_and_investments = categorise_by_sector(df)
    fig = go.Figure(data=[go.Pie(labels=list(sector_and_investments.keys()), values=list(sector_and_investments.values()))])

    fig.show()
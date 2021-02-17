import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd

import data_extracter
import expense_sheet_generator as esg
import investment_sheet_generator as isg
import style_generator

# Maybe will have to read all files and do for each file
de_expenses = data_extracter.DataExtracter('Expenses/2021/January.csv')
de_investments = pd.read_csv('Investments/Robinhood.csv')
df = de_expenses.get_df()
month = de_expenses.month
year = de_expenses.year

category_Total = esg.ExpenseSheetGenerator(df, 'Expenses in ' + month + ' based on Category', 'Category', 'ALL', '$')
category_USD = esg.ExpenseSheetGenerator(df, 'Expenses in ' + month + ' based on Category', 'Category', 'USD', '$')
category_INR = esg.ExpenseSheetGenerator(df, 'Expenses in ' + month + ' based on Category', 'Category', 'INR', '₹')
category_EUR = esg.ExpenseSheetGenerator(df, 'Expenses in ' + month + ' based on Category', 'Category', 'EUR', '€')

investment_USD = isg.InvestmentSheetGenerator(de_investments, 'Investments')

sg = style_generator.StyleGenerator()
sg.setSidebarStyle(position="fixed", width="16rem", padding="2rem 1rem", backgroundcolor="#f8f9fa")
sg.setContentStyle(marginleft="18rem", marginright="2rem", padding="2rem 1rem")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

sidebar = html.Div(
    [
        html.H2('Harikrishnan Lakshmanan', className="display-6", style={'textAlign':'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Expenses", href="/expenses", active="exact", style={'textAlign':'center'}, external_link=True),
                dbc.NavLink("Investments", href="/investments", active="exact", style={'textAlign':'center'}, external_link=True),                
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=sg.getSidebarStyle(),
)

content = html.Div(id="page-content", children=[], style=sg.getContentStyle())

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

category = dbc.Tabs(
    [  
        dbc.Tab(category_Total.getSheet(), label="Total", className="mt-3"),        
        dbc.Tab(category_USD.getSheet(), label="USD", className="mt-3"),
        dbc.Tab(category_INR.getSheet(), label="INR", className="mt-3"),
        dbc.Tab(category_EUR.getSheet(), label="EUR", className="mt-3"),        
    ])

investments = dbc.Tabs(
    [  
        dbc.Tab(investment_USD.getSheet(), label="USD", className="mt-3"),
    ])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/expenses" or pathname == '/':
        return category
    if pathname == '/investments':
        return investments
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P("The pathname {pathname} was not recognised..."),
        ]
    )


if __name__=='__main__':
    app.run_server(debug=True, port=3000)

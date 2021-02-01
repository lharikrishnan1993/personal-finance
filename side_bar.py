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
import chart_generator
import sheet_generator
import style_generator

# Maybe will have to read all files and do for each file
de = data_extracter.DataExtracter('Expenses/2021/January.csv')
df = de.get_df()
month = de.month
year = de.year

category_USD = sheet_generator.SheetGenerator(df, 'Expenses in ' + month + ' based on Category', 'Category', 'USD', '$')
category_INR = sheet_generator.SheetGenerator(df, 'Expenses in ' + month + ' based on Category', 'Category', 'INR', '₹')
category_EUR = sheet_generator.SheetGenerator(df, 'Expenses in ' + month + ' based on Category', 'Category', 'EUR', '€')

payment_USD = sheet_generator.SheetGenerator(df, 'Expenses in ' + month + ' based on Payment Mode', 'Payment Mode', 'USD', '$')
payment_INR = sheet_generator.SheetGenerator(df, 'Expenses in ' + month + ' based on Payment Mode', 'Payment Mode', 'INR', '₹')
payment_EUR = sheet_generator.SheetGenerator(df, 'Expenses in ' + month + ' based on Payment Mode', 'Payment Mode', 'EUR', '€')

sg = style_generator.StyleGenerator()
sg.setSidebarStyle(position="fixed", width="16rem", padding="2rem 1rem", backgroundcolor="#f8f9fa")
sg.setContentStyle(marginleft="18rem", marginright="2rem", padding="2rem 1rem")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

sidebar = html.Div(
    [
        html.H2(month, className="display-6", style={'textAlign':'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Category", href="/", active="exact", style={'textAlign':'center'}, external_link=True),
                dbc.NavLink("Payment Mode", href="/paymentmode", active="exact", style={'textAlign':'center'}, external_link=True),                
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
        dbc.Tab(category_USD.getSheet(), label="USD", className="mt-3"),
        dbc.Tab(category_INR.getSheet(), label="INR", className="mt-3"),
        dbc.Tab(category_EUR.getSheet(), label="EUR", className="mt-3"),        
    ])

payment = dbc.Tabs(
    [  
        dbc.Tab(payment_USD.getSheet(), label="USD", className="mt-3"),
        dbc.Tab(payment_INR.getSheet(), label="INR", className="mt-3"),
        dbc.Tab(payment_EUR.getSheet(), label="EUR", className="mt-3"),        
    ])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return category
    elif pathname == "/paymentmode":
        return payment        
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P("The pathname {pathname} was not recognised..."),
        ]
    )


if __name__=='__main__':
    app.run_server(debug=True, port=3000)

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

# Maybe will have to read all files and do for each file
de = data_extracter.DataExtracter('Expenses/2020/December.csv')
df = de.get_df()
month = de.month
year = de.year

category = sheet_generator.SheetGenerator(df, 'Expenses in ' + month + ' based on Category', 'Category', 'Travel', True, True)
payment = sheet_generator.SheetGenerator(df, 'Expenses in ' + month + ' based on Payment Mode', 'Payment Mode', 'Cash', True, True)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2(month, className="display-6", style={'textAlign':'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Category", href="/", active="exact", style={'textAlign':'center'}),
                dbc.NavLink("Payment Mode", href="/paymentmode", active="exact", style={'textAlign':'center'}),                
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return category.getSheet()
    elif pathname == "/paymentmode":
        return payment.getSheet()        
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
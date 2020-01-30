import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import pickle
from dash.dependencies import Input, Output, State

external_stylesheets = ['assets/1_style.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.config.suppress_callback_exceptions = True
app.title = 'RFM Analysis'

server = app.server

# Importing datasets
superstore = pd.read_csv('datasets/superstore_clean.csv')
superstore_od_id = pd.read_csv('datasets/superstore_od_id.csv')
superstore_rfm = pd.read_csv('datasets/superstore_rfm.csv')
superstore_cluster = pd.read_csv('datasets/superstore_cluster.csv')

# Making another dataset
superstore_world = superstore_od_id.groupby('Country').agg({'Market' : pd.Series.unique,
                                                            'Sales' : 'sum',
                                                            'Profit' : 'sum',
                                                            'Shipping Cost' : 'sum'}).round(2)
superstore_world.reset_index(inplace = True)

# Importing clustering model
cluster_model = pickle.load(open('rfm_cluster.sav', 'rb'))

# Active PAGE
app.layout = html.Div(children = [
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'active page', style = {'overflow-x' : 'hidden'})])

# Home PAGE
home = [dbc.Navbar(
    ## Top navigation bar
    dbc.Container(children = [
        ### Brand logo
        html.A(html.Img(src =  'assets/web_logo.png', height = '40rem'), href = '/#'),
        ### Menu navigation bar
        dbc.Nav(children = [
            dbc.NavItem(dbc.NavLink('Home', href = '/#'), style = {'margin-right' : '3.125rem'}),
            dbc.DropdownMenu(children = [
                dbc.DropdownMenuItem('Superstore Data', href = '/data'),
                dbc.DropdownMenuItem('Visualization', href = '/visual')],
                nav = True, in_navbar = True, label = 'Data', style = {'margin-right' : '3.125rem'}),
            dbc.NavItem(dbc.NavLink('RFM', id = 'rfm', href = '/RFM'))],
            navbar = True, className = 'ml-auto', style = {'padding-top' : '0.625rem'})]),
            color = 'dark', dark = True, fixed = 'top', sticky = 'top', 
            style = {'border-bottom' : '0.1875rem solid orange','height' : '4.375rem'}),
    ## Body
    html.Div(children = [
        ### RFM explanation
        html.Div(children = dbc.Row(
            dbc.Col([
                html.H1('RFM Analysis'),
                html.P('''A marketing analysis tool used to identify a company's or an organization's best customers 
                        by using three quantitative measures which are Recency (R), Frequency (F), and Monetary (M).
                        The concept of recency, frequency, monetary value (RFM) is thought to date from an article 
                        by Jan Roelf Bult and Tom Wansbeek, "Optimal Selection for Direct Mail", 
                        published in a 1995 issue of Marketing Science. RFM analysis often supports the marketing adage 
                        that "80% of business comes from 20% of the customers."''')],
                        style = {'background-color' : 'rgb(255, 165, 0, 0.4)', 'border-left' : '0.625rem solid orange', 
                        'margin-top' : '3.125rem', 'padding' : '1.25rem 2.5rem 0.625rem 3.125rem'},
                width = {'size' : 8}),
                style = {'text-align' : 'justify', 'justify-content' : 'center'})),
        ### RFM Image
        html.Div(dbc.Col(html.Img(src = 'assets/rfm_img.png', height = '500rem'), 
            style = {'text-align' : 'center', 'margin-top' : '3.125rem', 'margin-bottom' : '2.5rem'}))]),
    ## Bottom navigation bar
    dbc.Navbar(children = [
        dbc.Container(children = [
            html.H5('Created by Susanto'),
            dbc.Col(html.H5('© 2019'), style = {'text-align' : 'right'})])],
        style = {'border-top' : '0.1875rem solid orange', 'height' : '3.75rem'})]

# Data PAGE
data = [dbc.Navbar(
    ## Top navigation bar
    dbc.Container(children = [
        ### Brand logo
        html.A(html.Img(src =  'assets/web_logo.png', height = '40rem'), href = '/#'),
        ### Menu navigation bar
        dbc.Nav(children = [
            dbc.NavItem(dbc.NavLink('Home', href = '/#'), style = {'margin-right' : '3.125rem'}),
            dbc.DropdownMenu(children = [
                dbc.DropdownMenuItem('Superstore Data', href = '/data'),
                dbc.DropdownMenuItem('Visualization', href = '/visual')],
                nav = True, in_navbar = True, label = 'Data', style = {'margin-right' : '3.125rem'}),
            dbc.NavItem(dbc.NavLink('RFM', id = 'rfm', href = '/RFM'))],
            navbar = True, className = 'ml-auto', style = {'padding-top' : '0.625rem'})]),
            color = 'dark', dark = True, fixed = 'top', sticky = 'top', 
            style = {'border-bottom' : '0.1875rem solid rgb(52,204,235)','height' : '4.375rem'}),
    ## Body
    html.Div(
        html.Center(html.H2('Superstore Data', style = {'margin-top' : '0.3125rem', 'margin-bottom' : '0.625rem'})),
        style = {'border-bottom' : '0.1875rem solid rgb(52, 204, 235)'}),
        ### Options
        html.Div(children = [
            dbc.Row(children = [
                dbc.Col(html.P('Entries shown per page (max. 20): '), width = {'size' : 3}),
                dbc.Col(dcc.Input(id = 'entry_1', type = 'number', min = 5, max = 20, value = 10))], 
                style = {'padding-top' : '1.25rem'}),
            dbc.Row(children = [
                dbc.Col(html.P('Reset after sorting / filtering: '), width = {'size' : 3}),
                dbc.Col(html.Button('Reset', id = 'reset_1'))],
                style = {'padding-top' : '0.25rem', 'padding-bottom' : '0.625rem'}),
        ### DataTable
        html.Div(id = 'data_table_1', children = dash_table.DataTable(
            id = 'data_clean',
            columns = [{'name' : i, 'id' : i} for i in superstore.columns],
            style_header = {'backgroundColor': 'rgb(52, 204, 235)', 'fontWeight': 'bold'},
            style_table = {'overflowX': 'scroll'},
            style_cell = {'textAlign': 'left'},
            style_cell_conditional=[{'if': {'column_id': 'Order Date'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Order ID'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Customer Name'}, 'width': '9.375rem'},
                                    {'if': {'column_id': 'Customer ID'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Segment'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Country'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Market'}, 'width': '4.6875rem'},
                                    {'if': {'column_id': 'Product ID'}, 'width': '9.375rem'},
                                    {'if': {'column_id': 'Category'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Sub-Category'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Product Name'}, 'width': '18.75rem'},
                                    {'if': {'column_id': 'Item Price'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Quantity'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Discount'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Sales'}, 'width': '4.6875rem'},
                                    {'if': {'column_id': 'Profit'}, 'width': '4.6875rem'},
                                    {'if': {'column_id': 'Ship Mode'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Elapsed Time'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Shipping Cost'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Order Priority'}, 'width': '7.8125rem'}],
            data = superstore.to_dict('records'),
            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            page_action = 'native',
            sort_action = 'native',
            sort_mode = 'multi',
            filter_action = 'native',
            page_current = 0,
            page_size = 10)),
        ### Download Original Data
        dbc.Row(children = [
            html.P('Download the original data via'),
            html.Div(html.A(html.Img(src = 'assets/kaggle.png', height = '20rem'), 
                href = 'https://www.kaggle.com/jr2ngb/superstore-data', target = '_blank'),
                style = {'margin-left' : '0.3125rem'})]),
        ### Description
        html.Div(children = 
            dbc.Col(
                dcc.Markdown('''
                ### Description
                This data is retail dataset of a global superstore for 4 years (2011 - 2014).
                Data shown on the above table has been processed. 
                For the original data, refer to the provided link on _Kaggle_.

                Below is the description of each feature within the superstore data.
                * **Order Date:** Date when transaction occurred
                * **Order ID:** Identification for each unique transaction
                * **Customer Name:** Name of customer doing transaction
                * **Customer ID:** Identification for each unique customer
                * **Segment:** Segment of the customer
                * **Country:** Destination country for each transaction
                * **Market:** Market for the country
                * **Product ID:** Identification for each unique product
                * **Category:** Category of the product
                * **Sub-Category:** Sub-category of the product
                * **Product Name:** Detail name of the product
                * **Item Price:** Retail price for one unit of a product
                * **Quantity:** Amount of product bought in one transaction
                * **Discount:** Discount given for a product
                * **Sales:** Total amount paid by customer deducted by discount
                * **Profit:** Profit gained by the store for a product in one transaction
                * **Ship Mode:** Shipping mode for one transaction
                * **Elapsed Time:** Elapsed time between order date and shipping date
                * **Shipping Cost:** Cost of shipping (not included in sales)
                * **Order Priority:** Priority of one transaction  
                '''),
            style = {'text-align' : 'justify', 'background-color' : 'rgb(52, 204, 235, 0.4)', 
                'margin-top' : '3.125rem', 'margin-bottom' : '3.125rem', 'padding' : '1.25rem 2.5rem 0.625rem 2.5rem'},
            width = {'size' : 8, 'offset' : 2}))],
            style = {'max-width' : '68.75rem', 'margin' : '0 auto'}),
    ## Bottom navigation bar
    dbc.Navbar(children = [
        dbc.Container(children = [
            html.H5('Created by Susanto'),
            dbc.Col(html.H5('© 2019'), style = {'text-align' : 'right'})])],
        style = {'border-top' : '0.1875rem solid rgb(52, 204, 235)', 'height' : '3.75rem'})]

# Callback Entries Data
@app.callback(
    Output(component_id = 'data_clean', component_property = 'page_size'),
    [Input(component_id = 'entry_1', component_property = 'value')])

def entry_1(value):
    return value
 
# Callback Reset Data
@app.callback(
    Output(component_id = 'data_table_1', component_property = 'children'),
    [Input(component_id = 'reset_1', component_property = 'n_clicks')])

def reset_1(n_clicks):
    return dash_table.DataTable(
        id = 'data_clean',
        columns = [{'name' : i, 'id' : i} for i in superstore.columns],
        style_header = {'backgroundColor': 'rgb(52, 204, 235)', 'fontWeight': 'bold'},
        style_table = {'overflowX': 'scroll'},
        style_cell = {'textAlign': 'left'},
        style_cell_conditional=[{'if': {'column_id': 'Order Date'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Order ID'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Customer Name'}, 'width': '9.375rem'},
                                {'if': {'column_id': 'Customer ID'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Segment'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Country'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Market'}, 'width': '4.6875rem'},
                                {'if': {'column_id': 'Product ID'}, 'width': '9.375rem'},
                                {'if': {'column_id': 'Category'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Sub-Category'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Product Name'}, 'width': '18.75rem'},
                                {'if': {'column_id': 'Item Price'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Quantity'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Discount'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Sales'}, 'width': '4.6875rem'},
                                {'if': {'column_id': 'Profit'}, 'width': '4.6875rem'},
                                {'if': {'column_id': 'Ship Mode'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Elapsed Time'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Shipping Cost'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Order Priority'}, 'width': '7.8125rem'}],
        data = superstore.to_dict('records'),
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
        page_action = 'native',
        sort_action = 'native',
        sort_mode = 'multi',
        filter_action = 'native',
        page_current = 0,
        page_size = 10)

# Visualization PAGE
visual = [dbc.Navbar(
    ## Top navigation bar
    dbc.Container(children = [
        ### Brand logo
        html.A(html.Img(src =  'assets/web_logo.png', height = '40rem'), href = '/#'),
        ### Menu navigation bar
        dbc.Nav(children = [
            dbc.NavItem(dbc.NavLink('Home', href = '/#'), style = {'margin-right' : '3.125rem'}),
            dbc.DropdownMenu(children = [
                dbc.DropdownMenuItem('Superstore Data', href = '/data'),
                dbc.DropdownMenuItem('Visualization', href = '/visual')],
                nav = True, in_navbar = True, label = 'Data', style = {'margin-right' : '3.125rem'}),
            dbc.NavItem(dbc.NavLink('RFM', id = 'rfm', href = '/RFM'))],
            navbar = True, className = 'ml-auto', style = {'padding-top' : '0.625rem'})]),
            color = 'dark', dark = True, fixed = 'top', sticky = 'top', 
            style = {'border-bottom' : '0.1875rem solid rgb(255, 41, 41)','height' : '4.375rem'}),
    ## Body
    html.Div(html.Center(html.H2('Data Visualization', style = {'margin-top' : '0.3125rem', 'margin-bottom' : '0.625rem'})),
        style = {'border-bottom' : '0.1875rem solid rgb(255, 41, 41)'}),
        ### Options
        html.Div(children = [
            dbc.Row(children = [
                dbc.Col(html.P('Entries shown per page (max. 20): '), width = {'size' : 3}),
                dbc.Col(dcc.Input(id = 'entry_2', type = 'number', min = 5, max = 20, value = 10))], 
                style = {'padding-top' : '1.25rem'}),
            dbc.Row(children = [
                dbc.Col(html.P('Reset after sorting / filtering: '), width = {'size' : 3}),
                dbc.Col(html.Button('Reset', id = 'reset_2'))],
                style = {'padding-top' : '0.25rem', 'padding-bottom' : '0.25rem'}),   
            dcc.Markdown('''**Note:** The data presented below has been grouped based on Order ID to show each transaction.'''),
        ### DataTable
        html.Div(id = 'data_table_2', children = dash_table.DataTable(
            id = 'data_group_id',
            columns = [{'name' : i, 'id' : i} for i in superstore_od_id.drop(['Day', 'Date', 'Month', 'Year'], axis = 1).columns],
            style_header = {'backgroundColor': 'rgb(255, 41, 41)', 'fontWeight': 'bold'},
            style_table = {'overflowX': 'scroll'},
            style_cell = {'textAlign': 'left'},
            style_cell_conditional=[{'if': {'column_id': 'Order Date'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Order ID'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Customer Name'}, 'width': '9.375rem'},
                                    {'if': {'column_id': 'Customer ID'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Segment'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Country'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Market'}, 'width': '4.6875rem'},
                                    {'if': {'column_id': 'Category'}, 'width': '14.0625rem'},
                                    {'if': {'column_id': 'Quantity'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Sales'}, 'width': '4.6875rem'},
                                    {'if': {'column_id': 'Profit'}, 'width': '4.6875rem'},
                                    {'if': {'column_id': 'Ship Mode'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Elapsed Time'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Shipping Cost'}, 'width': '7.8125rem'},
                                    {'if': {'column_id': 'Order Priority'}, 'width': '7.8125rem'}],
            data = superstore_od_id.drop(['Day', 'Date', 'Month', 'Year'], axis = 1).to_dict('records'),
            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            page_action = 'native',
            sort_action = 'native',
            sort_mode = 'multi',
            filter_action = 'native',
            page_current = 0,
            page_size = 10)),
        ### Tabs
        html.Div(dcc.Tabs(children = [
            #### Tab Bar Chart
            dcc.Tab(label = 'Bar Chart', className = 'col-3', children = 
                html.Div(children = [
                dbc.Row([
                    dbc.Col(html.P('Variable:', style = {'font-size' : 20}), width = {'size' : 2}),
                    dbc.Col(dcc.Dropdown(id = 'bar_var', options = [{'label' : 'Segment', 'value' : 'Segment'},
                                                                    {'label' : 'Market', 'value' : 'Market'},
                                                                    {'label' : 'Category', 'value' : 'Category'},
                                                                    {'label' : 'Ship Mode', 'value' : 'Ship Mode'},
                                                                    {'label' : 'Elapsed Time', 'value' : 'Elapsed Time'},
                                                                    {'label' : 'Order Priority', 'value' : 'Order Priority'},
                                                                    {'label' : 'Day', 'value' : 'Day'},
                                                                    {'label' : 'Date', 'value' : 'Date'},
                                                                    {'label' : 'Month', 'value' : 'Month'},
                                                                    {'label' : 'Year', 'value' : 'Year'}],
                    value = 'Year', clearable = False), width = {'size' : 2})]),
                dcc.Graph(id = 'bar_graph')], 
                style = {'padding' : '1.25rem'}),
                selected_style = {'border-top': '0.0625rem solid rgb(214, 214, 214)', 'border-bottom': '0.1875rem solid rgb(255, 41, 41)'}),
            #### Tab Word Cloud
            dcc.Tab(label = 'Word Cloud', className = 'col-3', children = [
                html.Div(children = [
                    html.H3('Which products mostly bought by the customers?'),
                    dbc.Col(html.Img(src = 'assets/wordcloud.png', height = '300rem', 
                    style = {'margin-top' : '1.25rem'}), style = {'text-align' : 'center'})], 
                    style = {'padding' : '1.25rem', 'margin-bottom' : '0.625rem'})],
                    selected_style = {'border-top': '0.0625rem solid rgb(214, 214, 214)', 'border-bottom': '0.1875rem solid rgb(255, 41, 41)'}),
            #### Tab World Map
            dcc.Tab(label = 'World Map', className = 'col-3', children = 
                html.Div(children = [
                    dbc.Row([
                    dbc.Col(html.P('Variable:', style = {'font-size' : 20}), width = {'size' : 2}),
                    dbc.Col(dcc.Dropdown(id = 'world_var', options = [{'label' : 'Sales', 'value' : 'Sales'},
                                                                    {'label' : 'Profit', 'value' : 'Profit'},
                                                                    {'label' : 'Shipping Cost', 'value' : 'Shipping Cost'}],
                    value = 'Sales', clearable = False), width = {'size' : 2})]),
                    dbc.Row([
                    dbc.Col(html.P('Market:', style = {'font-size' : 20}), width = {'size' : 2}),
                    dbc.Col(dcc.Dropdown(id = 'world_mar', options = [{'label' : 'All', 'value' : 'All'},
                                                                    {'label' : 'US', 'value' : 'US'},
                                                                    {'label' : 'Canada', 'value' : 'Canada'},
                                                                    {'label' : 'LATAM', 'value' : 'LATAM'},
                                                                    {'label' : 'EU', 'value' : 'EU'},
                                                                    {'label' : 'EMEA', 'value' : 'EMEA'},
                                                                    {'label' : 'Africa', 'value' : 'Africa'},
                                                                    {'label' : 'APAC', 'value' : 'APAC'}],
                    value = 'All', clearable = False), width = {'size' : 2})]),
                    dcc.Graph(id = 'world_map')], 
                style = {'padding' : '1.25rem'}),
                selected_style = {'border-top': '0.0625rem solid rgb(214, 214, 214)', 'border-bottom': '0.1875rem solid rgb(255, 41, 41)'})], 
            content_style = {'border' : '0.0625rem solid #d6d6d6'}), 
            style = {'padding-top' : '4.6875rem', 'margin-bottom' : '3.125rem'})], 
            style = {'max-width' : '68.75rem', 'margin' : '0 auto'}),
    ## Bottom navigation bar
    dbc.Navbar(children = [
        dbc.Container(children = [
            html.H5('Created by Susanto'),
            dbc.Col(html.H5('© 2019'), style = {'text-align' : 'right'})])],
        style = {'border-top' : '0.1875rem solid rgb(255, 41, 41)', 'height' : '3.75rem'})]

# Callback Entries Visual
@app.callback(
    Output(component_id = 'data_group_id', component_property = 'page_size'),
    [Input(component_id = 'entry_2', component_property = 'value')])

def entry_2(value):
    return value
 
# Callback Reset Visual
@app.callback(
    Output(component_id = 'data_table_2', component_property = 'children'),
    [Input(component_id = 'reset_2', component_property = 'n_clicks')])

def reset_2(n_clicks):
    return dash_table.DataTable(
        id = 'data_group_id',
        columns = [{'name' : i, 'id' : i} for i in superstore_od_id.drop(['Day', 'Date', 'Month', 'Year'], axis = 1).columns],
        style_header = {'backgroundColor': 'rgb(255, 41, 41)', 'fontWeight': 'bold'},
        style_table = {'overflowX': 'scroll'},
        style_cell = {'textAlign': 'left'},
        style_cell_conditional=[{'if': {'column_id': 'Order Date'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Order ID'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Customer Name'}, 'width': '9.375rem'},
                                {'if': {'column_id': 'Customer ID'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Segment'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Country'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Market'}, 'width': '4.6875rem'},
                                {'if': {'column_id': 'Category'}, 'width': '14.0625rem'},
                                {'if': {'column_id': 'Quantity'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Sales'}, 'width': '4.6875rem'},
                                {'if': {'column_id': 'Profit'}, 'width': '4.6875rem'},
                                {'if': {'column_id': 'Ship Mode'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Elapsed Time'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Shipping Cost'}, 'width': '7.8125rem'},
                                {'if': {'column_id': 'Order Priority'}, 'width': '7.8125rem'}],
        data = superstore_od_id.drop(['Day', 'Date', 'Month', 'Year'], axis = 1).to_dict('records'),
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
        page_action = 'native',
        sort_action = 'native',
        sort_mode = 'multi',
        filter_action = 'native',
        page_current = 0,
        page_size = 10)

# Callback Tab Bar
@app.callback(
    Output(component_id = 'bar_graph', component_property = 'figure'),
    [Input(component_id = 'bar_var', component_property = 'value')])

def bar(value):
    return {'data' : [
        {'x' : superstore_od_id[value].value_counts(sort = False).keys(), 
        'y' : superstore_od_id[value].value_counts(sort = False).values,
        'type' : 'bar', 'name' : value}],
        'layout' : {'title' : f'Amount of Transactions based on {value}'}} 
    
# Callback Tab World
@app.callback(
    Output(component_id = 'world_map', component_property = 'figure'),
    [Input(component_id = 'world_var', component_property = 'value'),
    Input(component_id = 'world_mar', component_property = 'value')])

def world(var, mar):
    center_map = {'All' : {'lat' : 0, 'lon' : 0},
                    'US' : {'lat' : 48.9672, 'lon' : -118.7716},
                    'Canada' : {'lat' : 62.1304, 'lon' : -97.3468},
                    'LATAM' : {'lat' : -11.2894, 'lon' : -81.2109},
                    'EU' : {'lat' : 58.5260, 'lon' : 8.2551},
                    'EMEA' : {'lat' : 50.5937, 'lon' : 95.9629},
                    'Africa' : {'lat' : 0.7832, 'lon' : 14.5085},
                    'APAC' : {'lat' : 3.2088, 'lon' : 74.8456}}
    scale_map = {'All' : 1, 'US' : 3, 'Canada' : 3.5, 'LATAM' : 1.8, 'EU' : 3.8, 'EMEA' : 2, 'Africa' : 2.3, 'APAC' : 1.7}
    if mar == 'All':
        data_world = superstore_world
    else:
        data_world = superstore_world[superstore_world['Market'] == mar]
    return {'data' : [
                {'type' : 'choropleth', 'autocolorscale' : True, 'reversescale' : False, 
                'locations' : data_world['Country'], 'locationmode' : 'country names', 
                'marker' : {'line' : {'color' : 'darkgray', 'width' : 0.5}}, 
                'colorbar' : {'title' : {'text' : f'{var} USD'}, 'tickprefix' : 'USD '},
                'z' : data_world[var]}],    
            'layout' : {'title' : {'text' : f'Superstore {var} on {mar} Market(s) in 2011 - 2014'},
                'geo' : {'showframe' : True, 'showcoastlines' : False, 'showcountries' : True, 
                        'showocean' : True, 'oceancolor' : '#99FFFF', 'center' : center_map[mar], 
                        'projection' : {'type' : 'equirectangular', 'scale' : scale_map[mar]}}}}

# RFM PAGE
RFM = [dbc.Navbar(
    ## Top navigation bar
    dbc.Container(children = [
        ### Brand logo
        html.A(html.Img(src =  'assets/web_logo.png', height = '40rem'), href = '/#'),
        ### Menu navigation bar
        dbc.Nav(children = [
            dbc.NavItem(dbc.NavLink('Home', href = '/#'), style = {'margin-right' : '3.125rem'}),
            dbc.DropdownMenu(children = [
                dbc.DropdownMenuItem('Superstore Data', href = '/data'),
                dbc.DropdownMenuItem('Visualization', href = '/visual')],
                nav = True, in_navbar = True, label = 'Data', style = {'margin-right' : '3.125rem'}),
            dbc.NavItem(dbc.NavLink('RFM', id = 'rfm', href = '/RFM'))],
            navbar = True, className = 'ml-auto', style = {'padding-top' : '0.625rem'})]),
            color = 'dark', dark = True, fixed = 'top', sticky = 'top', 
            style = {'border-bottom' : '0.1875rem solid rgb(50, 205, 50)','height' : '4.375rem'}),
    ## Body
    html.Div(html.Center(html.H2('RFM Analysis', style = {'margin-top' : '0.3125rem', 'margin-bottom' : '0.625rem'})),
        style = {'border-bottom' : '0.1875rem solid rgb(50, 205, 50)'}),
        ### Options
        html.Div(children = [
            dbc.Row(children = [
                dbc.Col(html.P('Entries shown per page (max. 20): '), width = {'size' : 3}),
                dbc.Col(dcc.Input(id = 'entry_3', type = 'number', min = 5, max = 20, value = 10))], 
                style = {'padding-top' : '1.25rem'}),
            dbc.Row(children = [
                dbc.Col(html.P('Reset after sorting / filtering: '), width = {'size' : 3}),
                dbc.Col(html.Button('Reset', id = 'reset_3'))],
                style = {'padding-top' : '0.25rem', 'padding-bottom' : '0.625rem'}),
        ### DataTable
        html.Div(dbc.Row(children = [
            dbc.Col(id = 'data_table_3', children = dash_table.DataTable(
            id = 'data_rfm',
            columns = [{'name' : i, 'id' : i} for i in superstore_rfm[['Customer Name', 'Recency', 'Frequency', 'Monetary']].columns],
            style_header = {'backgroundColor': 'rgb(50, 205, 50)', 'fontWeight': 'bold'},
            style_cell = {'textAlign': 'left'},
            style_cell_conditional=[{'if': {'column_id': 'Customer Name'}, 'width': '9.375rem'},
                                    {'if': {'column_id': 'Recency'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Frequency'}, 'width': '6.25rem'},
                                    {'if': {'column_id': 'Monetary'}, 'width': '6.25rem'}],
            data = superstore_rfm[['Customer Name', 'Recency', 'Frequency', 'Monetary']].to_dict('records'),
            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            page_action = 'native',
            sort_action = 'native',
            sort_mode = 'multi',
            filter_action = 'native',
            page_current = 0,
            page_size = 10), 
            width = {'size' : 5}),
        ### Description
        dbc.Col(
            dcc.Markdown('''
            # Description
            Table on the left summarized each analyzed feature (RFM) of each customer. 
            Below is explanation of each feature.
            * **Customer Name:** Name of a customer
            * **Recency (Days):** Amount of days since last purchase date to 1 January 2015
            * **Frequency (Times):** Amount of transaction done by a customer since 2011
            * **Monetary (USD):** Amount of money spent by a customer on all transactions

            *Tip: Sort the datas to know your best customers (top 5, top 10, etc.) based on your desired feature.
            Remember that **Recency** is different with the other features (The best customer has small recency,
            high frequency, and high monetary).*
            '''),
            style = {'text-align' : 'justify',
                'background-color' : 'rgb(50, 205, 50, 0.4)', 'border-left' : '0.625rem solid rgb(50, 205, 50)',
                'padding' : '1.25rem 1.875rem 0.625rem 1.875rem', 'margin-left' : '0.625rem'})])),
        ### Pie chart
        html.Div(dbc.Row(children = [dbc.Col(dcc.Graph(
            figure = {
                'data' : [
                    go.Pie(
                        values = [superstore_cluster.groupby('Cluster').count()['Recency'][i] for i in range(1, 4)],
                        labels = [f'Cluster {i}' for i in range(1, 4)], sort = False)],
                'layout' : {'title' : 'Customer Segmentation (Clusters)'}}), 
            width = {'size' : 7}),
        ### Data Cluster
        dbc.Col(children = [
            dbc.Row(children = [
                dbc.Col(html.P('Choose cluster: ', style = {'font-size' : 20}), width = {'size' : 5}),
                dbc.Col(dcc.Dropdown(id = 'cluster_var', options = [{'label' : 'Cluster 1', 'value' : 1},
                                                                    {'label' : 'Cluster 2', 'value' : 2},
                                                                    {'label' : 'Cluster 3', 'value' : 3},
                                                                    {'label' : 'Others', 'value' : 'Others'}],
                value = 1, clearable = False),
                width = {'size' : 5})], style = {'padding-bottom' : '0.625rem'}),
                dash_table.DataTable(
                    id = 'data_cluster',
                    columns = [{'name' : i, 'id' : i} for i in superstore_rfm[['Customer Name', 'Recency', 'Frequency', 'Monetary']].columns],
                    style_header = {'backgroundColor': 'rgb(50, 205, 50)', 'fontWeight': 'bold'},
                    style_cell = {'textAlign': 'left'},
                    style_cell_conditional=[{'if': {'column_id': 'Customer Name'}, 'width': '9.375rem'},
                                            {'if': {'column_id': 'Recency'}, 'width': '6.25rem'},
                                            {'if': {'column_id': 'Frequency'}, 'width': '6.25rem'},
                                            {'if': {'column_id': 'Monetary'}, 'width': '6.25rem'}],
                    data = superstore_cluster[superstore_cluster['Cluster'] == 1][['Customer Name', 'Recency', 'Frequency', 'Monetary']].to_dict('records'),
                    style_data={'whiteSpace': 'normal', 'height': 'auto'},
                    page_action = 'native',
                    sort_action = 'native',
                    sort_mode = 'multi',
                    filter_action = 'native',
                    page_current = 0,
                    page_size = 10)], 
                    style = {'padding-top' : '1.875rem'})]), style = {'margin-top' : '0.625rem'}),
        ### Description
        html.Div(children = [
            dbc.Row(children = [
                #### Cluster 1
                dbc.Col(
                    dcc.Markdown('''
                    ### Cluster 1  
                    ### (Best Customers)
                    Customers in this cluster has low recency, high frequency, and high monetary.
                    It means that these customers just purchased recently, frequently purchased in the past,
                    and spent a good amount of money from our store. There are 317 customers (40%) within this cluster.

                    ###### Recommended Action:
                    Reward these customers by giving them early access to new products to help promoting new products from the store.
                    '''),
                    width = {'size' : 3}, 
                    style = {'text-align' : 'justify', 'background-color' : 'rgb(52, 204, 235, 0.8)', 
                            'padding-top' : '0.625rem', 'margin-right' : '1.875rem'}),
                #### Cluster 2
                dbc.Col(
                    dcc.Markdown('''
                    ### Cluster 2 
                    ### (Loyalist Customers)
                    Customers in this cluster has low recency, low frequency, and low monetary.
                    It means that these customers just purchased recently however they rarely purchased in the past
                    and spent a smaller amount of money from the store. There are 368 customers (46.5%) within this cluster.

                    ###### Recommended Action:
                    Offer membership or recommend related products to encourage these customers to buy more frequently
                    with better amount of money.
                    '''),
                    width = {'size' : 3}, 
                    style = {'text-align' : 'justify', 'background-color' : 'rgb(255, 165, 0, 0.8)', 
                            'padding-top' : '0.625rem', 'margin-right' : '1.875rem'}),
                #### Cluster 3
                dbc.Col(
                    dcc.Markdown('''
                    ### Cluster 3 
                    ### (At Risk Customers)
                    Customers in this cluster has high recency. It means that these customers have not purchased from the store
                    for quite some time. In this cluster, there are customers with low frequency-monetary and high frequency-monetary.
                    Further action should be carried out to distinguish them. There are 107 customers (13.5%) within this cluster.
                    
                    ###### Recommended Action:
                    Offer relevant promotion to returning customers and if necessary, conduct surveys to find out why the customers
                    have not purchased from the store.
                    '''),
                    width = {'size' : 3}, 
                    style = {'text-align' : 'justify',
                            'background-color' : 'rgb(50, 205, 50, 0.8)', 'padding-top' : '0.625rem'})], 
                style = {'justify-content' : 'center', 'margin-top' : '1.25rem'}),
            #### Lost Customers
            html.Div(children = dbc.Col(
                dcc.Markdown('''
                ### Lost Customers
                There are 3 customers that cannot be grouped within the 3 clusters. They are Nicole Brennan,
                Robert Barroso, and Shirley Jackson. These customers have extremely high recency which means
                they have not purchased from the store for a long time.

                ###### Recommended Action:
                Do the same with customers on cluster 3. If there is no response, focus on the other customers
                within the 3 clusters.  
                '''),
                width = {'size' : 10, 'offset' : 1},
                style = {'text-align' : 'justify', 'background-color' : 'rgb(255, 41, 41, 0.8)', 
                        'padding-top' : '0.625rem', 'padding-bottom' : '0.3125rem'}),
                style = {'margin-top' : '1.875rem'})]),
        ### Tabs
        html.Div(dcc.Tabs(id = 'tabs 2', children = [
            #### Tab Clusters
            dcc.Tab(label = 'KDE Plot', className = 'col-3', children = [
                dbc.Col(dcc.Markdown('''
                KDE plots below show distribution of Recency, Frequency, Monetary for each cluster.
                It should be noted since the datas plotted in those charts are scaled data, all features have the same attribute
                (the larger the value, the better is the customer).
                '''), 
                width = {'size' :10, 'offset' : 1}, 
                style = {'text-align' : 'justify', 'padding-top' : '1.25rem'}),
            html.Div(html.Img(src = 'assets/kde_plot.png'), style = {'padding' : '1.25rem', 'text-align' : 'center'})],
                selected_style = {'border-top': '0.0625rem solid rgb(214, 214, 214)', 'border-bottom': '0.1875rem solid rgb(50, 205, 50)'}),
            #### Tab Prediction
            dcc.Tab(label = 'Prediction', className = 'col-3', children = [
                dbc.Row(children = [
                    dbc.Col(children = [
                        html.H3('Know your Customer'),
                        ##### Input Recency
                        dbc.Row(children = [
                            dbc.Col(html.P('Last Purchase Date:', style = {'font-size' : 20})),
                            dbc.Col(dcc.DatePickerSingle(
                                id = 'recency', min_date_allowed = datetime(2011, 1, 1), max_date_allowed = datetime(2014, 12, 31),
                                initial_visible_month = datetime(2014, 12, 31), display_format = 'Y-M-D', 
                                placeholder = 'Select a Date'))], style = {'margin-top' : '0.625rem'}),
                        ##### Input Frequency
                        dbc.Row(children = [
                            dbc.Col(html.P('Total Number of Transactions:', style = {'font-size' : 20})),
                            dbc.Col(dcc.Input(
                                id = 'frequency', type = 'number', min = 1, placeholder = 'Input a number'))], 
                            style = {'margin-top' : '0.625rem'}),
                        ##### Input Monetary
                        dbc.Row(children = [
                            dbc.Col(html.P('Amount Spent (USD):', style = {'font-size' : 20})),
                            dbc.Col(
                                dcc.Input(id = 'monetary', type = 'number', min = 1, placeholder = 'Input a number'))]),
                        ##### Clustering Button
                        html.Div(html.Button('Cluster', id = 'cluster'), style = {'margin-left' : '25rem'})],
                        width = {'size' : 8}, 
                        style = {'padding-top' : '0.625rem'}),
                    ##### Prediction Output
                    dbc.Col(html.Div(id = 'predict_output'),
                    style = {'text-align' : 'justify',
                            'background-color' : 'rgb(50, 205, 50, 0.4)', 'padding-top' : '0.625rem'})], 
                style = {'margin' : '1.25rem 3.125rem', 'height' : '18.75rem'})],
                selected_style = {'border-top': '0.0625rem solid rgb(214, 214, 214)', 'border-bottom': '0.1875rem solid rgb(50, 205, 50)'})], 
            content_style = {'border' : '0.0625rem solid #d6d6d6'}), 
            style = {'padding-top' : '4rem', 'margin-bottom' : '3.125rem'})],
            style = {'max-width' : '68.75rem', 'margin' : '0 auto'}),
    ## Bottom navigation bar
    dbc.Navbar(children = [
        dbc.Container(children = [
            html.H5('Created by Susanto'),
            dbc.Col(html.H5('© 2019'), style = {'text-align' : 'right'})])],
        style = {'border-top' : '0.1875rem solid rgb(50, 205, 50)', 'height' : '3.75rem'})]

# Callback Entries Visual
@app.callback(
    Output(component_id = 'data_rfm', component_property = 'page_size'),
    [Input(component_id = 'entry_3', component_property = 'value')])

def entry_3(value):
    return value
 
# Callback Reset Visual
@app.callback(
    Output(component_id = 'data_table_3', component_property = 'children'),
    [Input(component_id = 'reset_3', component_property = 'n_clicks')])

def reset_3(n_clicks):
    return dash_table.DataTable(
        id = 'data_rfm',
        columns = [{'name' : i, 'id' : i} for i in superstore_rfm[['Customer Name', 'Recency', 'Frequency', 'Monetary']].columns],
        style_header = {'backgroundColor': 'rgb(50, 205, 50)', 'fontWeight': 'bold'},
        style_cell = {'textAlign': 'left'},
        style_cell_conditional=[{'if': {'column_id': 'Customer Name'}, 'width': '9.375rem'},
                                {'if': {'column_id': 'Recency'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Frequency'}, 'width': '6.25rem'},
                                {'if': {'column_id': 'Monetary'}, 'width': '6.25rem'}],
        data = superstore_rfm[['Customer Name', 'Recency', 'Frequency', 'Monetary']].to_dict('records'),
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
        page_action = 'native',
        sort_action = 'native',
        sort_mode = 'multi',
        filter_action = 'native',
        page_current = 0,
        page_size = 10)

# Callback Cluster Table
@app.callback(
    Output(component_id = 'data_cluster', component_property = 'data'),
    [Input(component_id = 'cluster_var', component_property = 'value')])

def choose_cluster(value):
    if value != 'Others':
        return superstore_cluster[superstore_cluster['Cluster'] == value][['Customer Name', 'Recency', 'Frequency', 'Monetary']].to_dict('records')
    else:
        superstore_ot = superstore_rfm.loc[[571, 642, 699]]
        return superstore_ot.drop('Inverse_Recency', axis = 1).to_dict('records')

# Callback Prediction Tab
@app.callback(
    Output(component_id = 'predict_output', component_property = 'children'),
    [Input(component_id = 'cluster', component_property = 'n_clicks')],
    [State(component_id = 'recency', component_property = 'date'),
    State(component_id = 'frequency', component_property = 'value'),
    State(component_id = 'monetary', component_property = 'value')])

def predict_cluster(n_clicks, r, f, m):
    try:
        r = r.split('-')
        r = (datetime(int(r[0]), int(r[1]), int(r[2])) - datetime(2010, 12, 31)).days
        prediction = cluster_model.predict(np.array([r, f, m]).reshape(1, -1))[0]
        if prediction == 0:
            return dcc.Markdown('''
            ##### Result:
            This is your **Best Customer**. Give them privilege such as early access to new products! 
            ''')
        elif prediction == 1:
            return dcc.Markdown('''
            ##### Result:
            This is your **Loyalist Customer**. Give them membership offering and other promotions
            so that they frequently spend more from the store.
            ''')
        else:
            return dcc.Markdown('''
            ##### Result:
            This is your **At Risk Customer**. Give them relevant promotions on related products and find out
            why they have not purchased from the store recently. Don't lose them!.
            ''')
    except:
        return html.H3('Please fill all values!', style = {'color' : 'red'}) 

# Callback page
@app.callback(
    Output(component_id = 'active page', component_property = 'children'),
    [Input(component_id = 'url', component_property = 'pathname')])

def display_page(pathname):
    if pathname == '/data':
        return data
    elif pathname == '/visual':
        return visual
    elif pathname == '/RFM':
        return RFM
    else:
        return home

if __name__ == '__main__':
    app.run_server(debug=True)
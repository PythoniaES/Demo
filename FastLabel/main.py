
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc
from dash.dependencies import Input, Output
import os
import dash_bootstrap_components as dbc

global df, title, x_buy, x_sell, y_buy, y_sell
# inizialization variables
x_buy, x_sell, y_buy, y_sell = [],[],[],[]
last_save=0
last_cancel=0
value = 'BTCEUR'
title = value
df = pd.read_csv('./DATA/{}.csv'.format(value))
df.start = pd.to_datetime(df.start)
df = df.sort_values('start')
df.index = df.start
fig = px.line(x=df.index, y=df['close']
    ).add_traces(
    px.line(x=df.index, y=df['close']
    )
        .update_traces(marker_color="rgba(0,0,0,0)").data
)
fig.layout.height = 400



tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dash.dcc.Graph(id="graph_1", figure=fig, ),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            dash.dcc.Graph(id="graph_2", figure=fig),
        ]
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Buy "),
        dbc.Tab(tab2_content, label="Sell"),

    ]
)

# Build App

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.layout = dash.html.Div([
    dbc.Row([
        dbc.Row(dbc.Card(dash.html.H1('FastTradingLabel'),color='danger')),
        dbc.Col([


            dbc.Row( [
        dbc.Row(dash.html.H6('FTL is a tool to quickly label cryptocurrency data,'
                             ' choose the exchange and click on the chart to the right'
                             'the market entry and exit points you consider appropriate')),
        dbc.Row(dash.html.H4('Select exchange')),
        dbc.Row(
                            dcc.Dropdown(
                                options=list({'label':x[:-4],'value':x} for x in os.listdir('DATA')), id='select_cripto',

                            )
                    ),

        dbc.Row( id='n_operation_buy'),
        dbc.Row( id='n_operation_sell'),
        dbc.Button('Cancel', n_clicks=0,id='cancel'),
        dbc.Button('Save', n_clicks=0,id='save'),
    ],
    className="d-grid gap-2 col-6 mx-auto",),
            dbc.Row(),
            dbc.Row( id='saved'),
        ],align="end"),
        dbc.Col(tabs,id='tab', width=8)
    ]),
    dbc.Row(dash.html.Div(id="where"))
])


@app.callback(
    Output("where", "children"),
    Output("n_operation_buy", "children"),
    Output("n_operation_sell", "children"),
    Input("graph_1", "clickData"),
    Input("graph_2", "clickData"),
    Input("save", 'n_clicks'),
    Input("cancel", 'n_clicks')
)
def click(clickData1,clickData2,save,cancel):
    global x_buy, x_sell, y_buy, y_sell, last_cancel, last_save

    if cancel == last_cancel and save == last_save:
        if clickData1:
            x_buy.append(clickData1['points'][0]['x'])
            y_buy.append(clickData1['points'][0]['y'])

        if clickData2:
            x_sell.append(clickData2['points'][0]['x'])
            y_sell.append(clickData2['points'][0]['y'])

    if cancel > last_cancel:
        last_cancel += 1

        if x_buy != []:
            x_buy.pop()
        if x_sell != []:
            x_sell.pop()
        if y_buy != []:
            y_buy.pop()
        if y_sell != []:
            y_sell.pop()

    if save > last_save:

        last_save += 1
        df['BUY']=0
        df['SELL'] = 0
        df['BUY'].loc[list(set(x_buy))] = 1
        df['SELL'].loc[list(set(x_sell))] = 1
        df.to_csv('./LABELED_DATA/{}.csv'.format(title), index=False)
        x_buy, x_sell, y_buy, y_sell = [], [], [], []

    trace = go.Candlestick(x=df.start,
                           open=df.open,
                           high=df.high,
                           low=df.low,
                           close=df.close)
    data = [trace]
    data.append(go.Scatter(x=x_buy, y=y_buy,
                               mode='markers',
                               name='buy',
                               marker_size=20,
                               marker_symbol="triangle-up",
                               marker_color="green"))
    data.append(go.Scatter(x=x_sell, y=y_sell,
                               mode='markers',
                               name='buy',
                               marker_size=20,
                               marker_symbol="triangle-down",
                               marker_color="red"))
    layout = {'title':title,'xaxis': {'rangeslider': {'visible': False}}}
    figure = {'data': data, 'layout': layout}

    return dash.dcc.Graph(figure=figure), dash.html.H4('Number of buy: {}'.format(str(len(set(x_buy))))),\
           dash.html.H4('Number of sell: {}\n'.format(str(len(set(x_sell)))))



@app.callback(
    (Output("tab", "children")),
    Input("select_cripto", 'value')
)
def drop(value):
    global df, title, x_buy, x_sell, y_buy, y_sell

    x_buy, x_sell, y_buy, y_sell = [], [], [], []
    ###### FIGURE TAB
    if not value:
        value = 'BTCEUR'
    else:
        value = value[:-4]
    title = value
    df = pd.read_csv('./DATA/{}.csv'.format(value))
    df.start = pd.to_datetime(df.start)
    df = df.sort_values('start')
    df.index = df.start
    fig = px.line(x=df.index, y=df['close']
                  ).add_traces(
        px.line(x=df.index, y=df['close']
                )
            .update_traces(marker_color="rgba(0,0,0,0)").data
    )
    fig.layout.height = 400
    tab1_content = dbc.Card(
        dbc.CardBody(
            [
                dash.dcc.Graph(id="graph_1", figure=fig),
            ]
        ),
        className="mt-3",
    )

    tab2_content = dbc.Card(
        dbc.CardBody(
            [
                dash.dcc.Graph(id="graph_2", figure=fig),
            ]
        ),
        className="mt-3",
    )

    tabs = dbc.Tabs(
        [
            dbc.Tab(tab1_content, label="Buy "),
            dbc.Tab(tab2_content, label="Sell"),

        ]
    )
    return tabs






# Run app and display result inline in the notebook
app.run_server()


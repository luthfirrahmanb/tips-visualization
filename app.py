import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from categoryplot import getPlot
from data import dfTips

app = dash.Dash()

app.title = 'Dash Si Tampan'
color_set = {
    'sex': ['#ff3fd8', '#4290ff'],
    'smoker': ['#99ffff', '#ac7339'],
    'time': ['#0033cc', '#ffff4d'],
    'day': ['#80ced6', '#66ff66', '#ff66d9', '#993300']
}

def generate_table(dataframe, max_rows=10):
    return html.Table(
        [html.Tr([html.Th(col, className='tableStyle') for col in dataframe.columns])] +

        [html.Tr([
            html.Td(dataframe.iloc[i][col], className='tableStyle') for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
        ,className='tableStyle'
    )

app.layout = html.Div(children=[
    dcc.Tabs(id='tabs', value= 'tab-2',
        style = {
            'fontFamily': 'system-ui'
        },
        content_style = {
            'fontFamily': 'Arial',
            'borderLeft': '1px solid #d6d6d6',
            'borderRight': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'padding': '44px'
        },
    children=[
        dcc.Tab(label='Tips data set', value= 'tab-1', children=[
            html.Div([
                html.H1(
                    children='Tips Data Set',
                    className='h1Tab'
                ),
                generate_table(dfTips)
            ])
        ]),
        dcc.Tab(label='Scatter Plot', value= 'tab-2', children=[
            html.Div([
                html.H1(
                    children='Scatter Plot Tips Data Set',
                    className='h1Tab'
                ),
                html.Table([
                    html.Tr([
                        html.Td(html.P('Hue: ')),
                        html.Td(
                            dcc.Dropdown(
                                id='ddl-hue-scatter',
                                options=[{'label': 'Smoker', 'value': 'smoker'},
                                        {'label': 'Sex', 'value': 'sex'},
                                        {'label': 'Day', 'value': 'day'},
                                        {'label': 'Time', 'value': 'time'}
                                ],
                                value='sex'
                            )
                        )
                    ])
                ], style={'width': '300px'}),
                dcc.Graph(
                        id='scatterPlot',
                        figure={
                            'data': []    
                        }
                    )
            ])
        ]),
        dcc.Tab(label='Categorical Plot', value= 'tab-3', children=[
            html.Div([
                html.H1(
                    children='Categorical Plot Tips Data Set',
                    className='h1Tab'
                ),
                html.Table([
                    html.Tr([
                        html.Td([
                            html.P('Jenis: '),
                            dcc.Dropdown(
                                id='ddl-jenis-plot-category',
                                options=[{'label': 'Bar', 'value': 'bar'},
                                        {'label': 'Violin', 'value': 'violin'},
                                        {'label': 'Box', 'value': 'box'}
                                ],
                                value='bar'
                            )
                        ]),
                        html.Td([
                            html.P('X Axis: '),
                            dcc.Dropdown(
                                id='ddl-x-plot-category',
                                options=[{'label': 'Smoker', 'value': 'smoker'},
                                        {'label': 'Sex', 'value': 'sex'},
                                        {'label': 'Day', 'value': 'day'},
                                        {'label': 'Time', 'value': 'time'}
                                ],
                                value='sex'
                            )
                        ])
                    ])
                ], style={'width': '900px'}),
                dcc.Graph(
                    id='categoricalPlot',
                    figure={
                        'data': []
                    }
                )
            ])
        ])
    ])
],
    style = {
        'maxWidth': '1000px',
        'margin': '0 auto'
    }
)

# Categorical graph callback

@app.callback(
    Output('categoricalPlot', 'figure'),
    [Input('ddl-jenis-plot-category', 'value'), Input('ddl-x-plot-category', 'value')]
)

def update_category_graph(ddljeniscategory, ddlxcategory):
   return {
       'data': getPlot(ddljeniscategory, ddlxcategory),
       'layout': go.Layout(
                    xaxis={'title': ddlxcategory.capitalize()}, yaxis={'title': 'US$'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1}, hovermode='closest',
                    boxmode='group', violinmode='group'
                    # plot_bgcolor= 'black', paper_bgcolor= 'black',
                )
   }

# scatter plot callback

@app.callback(
    Output('scatterPlot', 'figure'),
    [Input('ddl-hue-scatter', 'value')]
)

def update_scatter_hue(ddlhuescatter):
    return {
        'data': [
                go.Scatter(
                    x=dfTips[dfTips[ddlhuescatter] == col]['total_bill'], 
                    y=dfTips[dfTips[ddlhuescatter] == col]['tip'], 
                    mode='markers', 
                    # line=dict(color=color_set[i], width=1, dash='dash'),
                    marker=dict(color=color_set[ddlhuescatter][i], size=10, line={'width': 0.5, 'color': 'white'}), name=col)
                for col,i in zip(dfTips[ddlhuescatter].unique(),range(len(color_set[ddlhuescatter])))
            ],
            'layout': go.Layout(
                xaxis={'title': 'Total Bill'},
                yaxis={'title': 'Tip'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                hovermode='closest'
            )
    }


if __name__ == '__main__':
    app.run_server(debug=True, port=1996)
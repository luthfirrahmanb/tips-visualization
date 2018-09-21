import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from categoryplot import getPlot
from data import dfTips
import numpy as np

app = dash.Dash()

app.title = 'Dash Si Tampan'
color_set = {
    'sex': ['#ff3fd8', '#4290ff'],
    'smoker': ['#99ffff', '#ac7339'],
    'time': ['#0033cc', '#ffff4d'],
    'day': ['#80ced6', '#66ff66', '#ff66d9', '#993300']
}

estiFunc = {
    'count': len,
    'sum': sum,
    'mean': np.mean,
    'std': np.std
}

disabledEsti = {
   'count': True,
    'sum': False,
    'mean': False,
    'std': False 
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
    dcc.Tabs(id='tabs', value= 'tab-4',
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
                html.Div(html.P('', id='jml-data-scatter')),
                dcc.Graph(
                    id='scatterPlot',
                    figure={
                        'data': []    
                    }
                ),
                dcc.Slider(
                    id='size-scatter-slider',
                    min=dfTips['size'].min(),
                    max=dfTips['size'].max(),
                    value=dfTips['size'].min(),
                    marks={str(size): str(size) for size in dfTips['size'].unique()}
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
        ]),
        dcc.Tab(label='Pie Chart', value= 'tab-4', children=[
            html.Div([
                html.H1(
                    children='Pie Chart Tips Data Set',
                    className='h1Tab'
                ),
                html.Table([
                    html.Tr([
                        html.Td(html.P('Hue: ')),
                        html.Td(
                            dcc.Dropdown(
                                id='ddl-hue-pie',
                                options=[{'label': 'Smoker', 'value': 'smoker'},
                                        {'label': 'Sex', 'value': 'sex'},
                                        {'label': 'Day', 'value': 'day'},
                                        {'label': 'Time', 'value': 'time'}
                                ],
                                value='sex'
                            )
                        ),
                        html.Td(html.P('Estimator: ')),
                        html.Td(
                            dcc.Dropdown(
                                id='ddl-est-pie',
                                options=[{'label': 'Count', 'value': 'count'},
                                        {'label': 'Sum', 'value': 'sum'},
                                        {'label': 'Mean', 'value': 'mean'},
                                        {'label': 'Std', 'value': 'std'}
                                ],
                                value='count'
                            )
                        ),
                        html.Td(html.P('Column: ')),
                        html.Td(
                            dcc.Dropdown(
                                id='ddl-col-pie',
                                options=[{'label': 'Total Bill', 'value': 'total_bill'},
                                        {'label': 'Tip', 'value': 'tip'}
                                ],
                                value='total_bill',
                                disabled=True
                            )
                        )
                    ])
                ], style={'width': '900px'}),
                dcc.Graph(
                    id='piePlot',
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
    [Input('ddl-hue-scatter', 'value'), Input('size-scatter-slider', 'value')]
)

def update_scatter_hue(ddlhuescatter, size):
    return {
        'data': [
                go.Scatter(
                    x=dfTips[(dfTips[ddlhuescatter] == col) & (dfTips['size'] == size)]['total_bill'], 
                    y=dfTips[(dfTips[ddlhuescatter] == col) & (dfTips['size'] == size)]['tip'], 
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
# Perhitungan jumlah data

@app.callback(
    Output('jml-data-scatter', 'children'),
    [Input('size-scatter-slider', 'value')]
)

def update_scatter_jmlData(size):
    return 'Jumlah Data: ' + str(len(dfTips[dfTips['size'] ==  size]))


# Pie Callback
@app.callback(
    Output('ddl-col-pie', 'disabled'),
    [Input('ddl-est-pie', 'value')]
)

def update_disabled(disabled):
    return disabledEsti[disabled]


@app.callback(
     Output('piePlot', 'figure'),
    [Input('ddl-hue-pie', 'value'), Input('ddl-est-pie', 'value'), Input('ddl-col-pie', 'value')]
)


def update_pie_hue(ddlhuepie, est, col):
    return {
        'data': [
            go.Pie(labels=list(dfTips[ddlhuepie].unique()),
                    values=[estiFunc[est](dfTips[dfTips[ddlhuepie]==item][col]) for item in dfTips[ddlhuepie].unique()],
                    hoverinfo='label+percent', textinfo='value', 
                    textfont=dict(size=20),
                    marker=dict(colors=color_set[ddlhuepie], 
                    line=dict(color='#000000', width=2)))
        ],
        'layout': go.Layout(
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1}
        )
    }



if __name__ == '__main__':
    app.run_server(debug=True, port=1996)
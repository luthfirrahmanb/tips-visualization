import plotly.graph_objs as go
from data import dfTips

listGoFunc = {
    'bar': go.Bar,
    'violin': go.Violin,
    'box': go.Box
}

def getPlot(jenis, xCategory):
    return [
        listGoFunc[jenis](
            x=dfTips[xCategory],
            y=dfTips['tip'],
            text=dfTips['day'],
            opacity=0.7,
            name='Tip',
            marker=dict(color='blue'),
            legendgroup = 'tip'
        ),
        listGoFunc[jenis](
            x=dfTips[xCategory],
            y=dfTips['total_bill'],
            text=dfTips['day'],
            opacity=0.7,
            name='Total Bill',
            marker=dict(color='orange'),
            legendgroup = 'total_bill'
        )
    ]
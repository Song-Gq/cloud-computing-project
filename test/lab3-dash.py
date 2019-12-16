import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# read dataframe from .csv file
df = pd.read_csv(r'googleplaystore.csv',encoding='ANSI')

# illegal categories when creating scatter
illegalCatg = ['3.9', '4.3', '4.6', '4.5', '4.1', '4.7', '4', '4.2', '000+"',
               '3.7', '3.8', '3.1', '3.6', '4.4', '3', '1.9', '4.8', '2.7']
# dropdown list's values for max displayed in scatter
dropdown_val = [10, 50, 100, 500, 1000, 5000, 10000]
# radio items to choose x axis's log-or-linear type of distplot of price
radio_label = ['linear', 'log']

# create sorted arrays to build a bar chart for installs
amount_of_installs = []
installs_type = []
illegalInstalls = ['Paid', 'Free', 'Photography']
for i in df.Installs.unique():
    if i not in illegalInstalls:
        amount_of_installs.append(list(df.Installs).count(i))
        if i[-1] == '+':
            installs_type.append(int(i[:-1].replace(',','')))
        else:
            installs_type.append(int(i.replace(',','')))
z = zip(installs_type, amount_of_installs)
z = sorted(z, reverse=True)
installs_type, amount_of_installs = zip(*z)

# create an array for a pie chart of free-or-paid type
amount_of_type = []
type_list = ['Free', 'Paid']
for i in type_list:
    amount_of_type.append(list(df.Type).count(i))

# create arrays for a distplot of price
amount_of_price = []
group_labels = ['Price Distplot']
for i in df.Price:
    if i[0] == '$':
        amount_of_price.append(float(i[1:]))
fig = ff.create_distplot([amount_of_price], group_labels)
fig['layout'].update(xaxis={'title': 'Price(US Dollars)', 'type': 'linear'})


app.layout = html.Div(children=[
    # a dropdown list
    html.Div(children=[
        html.Br(),
        html.P('Max Displayed in Scatter:'),
        dcc.Dropdown(
            id='max-displayed',
            options=[{'label': i, 'value': i} for i in dropdown_val],
            value=50
        )
    ], style={'width': '30%', 'display': 'block', 'margin-left': '2%'}),

    # scatter
    html.Div(id='scatter-div', children=[
        dcc.Graph(
            id='rating-vs-reviews',
        )
    ], style={'width': '70%', 'display': 'inline-block'}),

    # pie chart of free-or-paid type
    html.Div(children=[
        dcc.Graph(
            id='type',
            figure={
                'data': [
                    go.Pie(labels=type_list, values=amount_of_type)
                ],
                'layout': go.Layout(
                )
            }
        )
    ], style={'width': '29%', 'display': 'inline-block'}),

    # radio items
    html.Div(children=[
        html.Br(),
        html.Br(),
        html.P('X Axis Type in Price Distplot:'),
        dcc.RadioItems(
            id='log-linear',
            options=[{'label': i, 'value': i} for i in radio_label],
            value='linear'
        )
    ], style={'margin-left': '3%', 'display': 'block'}),

    # a distplot of price
    html.Div(id='distplot-div', children=[
        dcc.Graph(
            id='price',
        )
    ], style={'width': '49%', 'display': 'inline-block'}),

    # bar chart of installs
    html.Div(children=[
        dcc.Graph(
            id='amount-vs-installs',
            figure={
                'data': [
                    {'x': installs_type, 'y': amount_of_installs, 'type': 'bar'}
                ],
                'layout': go.Layout(
                    xaxis={'title': 'Installs(Greater Than)', 'type': 'category'},
                    yaxis={'title': 'Amount'}
                )
            }
        )
    ], style={'width': '49%', 'float': 'right'})
])


# callback of the dropdown list, to adjust the maxdisplayed value of scatter
@app.callback(
    Output(component_id='rating-vs-reviews', component_property='figure'),
    [Input(component_id='max-displayed', component_property='value')]
)
def update_scatter(input_value):
    return {
        'data': [
            go.Scatter(
                x=df[df['Category'] == i]['Reviews'],
                y=df[df['Category'] == i]['Rating'],
                text=df[df['Category'] == i]['App'],
                mode='markers',
                opacity=0.5,
                marker={
                    'size': 10,
                    'line': {'width': 0.5, 'color': 'white'},
                    'maxdisplayed': input_value
                },
                name=i
            ) for i in df.Category.unique() if i not in illegalCatg
        ],
        'layout': go.Layout(
            xaxis={'title': 'Reviews', 'type': 'log'},
            yaxis={'title': 'Rating', 'range': [0, 5.1], 'fixedrange': True},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': -0.4, 'y': 0},
            hovermode='closest'
        )
    }

# callback of radio items, to adjust the log-or-linear type of x axis in distplot of price
@app.callback(
    Output(component_id='price', component_property='figure'),
    [Input(component_id='log-linear', component_property='value')]
)
def update_distplot(input_value):
    if(input_value == 'linear'):
        fig['layout'].update(xaxis={'type': 'linear'})
    else:
        fig['layout'].update(xaxis={'type': 'log'})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
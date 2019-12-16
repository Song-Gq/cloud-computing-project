import dash
import dash_core_components as dcc
import dash_html_components as html
from impala.dbapi import connect
from impala.util import as_pandas
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # {
    #     'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
    #     'rel': 'stylesheet',
    #     'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
    #     'crossorigin': 'anonymous'
    # }
]

# cursor.execute('select * from customer limit 100')
# df = pd.DataFrame(as_pandas(cursor))

def generate_table(dataframe, max_rows=100):
    return html.Table(
        html.Tbody(
            # Header
            [html.Tr([html.Th(col.split('.')[1:]) for col in dataframe.columns])] +
            # Body
            [html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))]
        )
    )

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Black Friday'),
    dcc.Dropdown(id='search-option',
        options=[
            {'label': 'user', 'value': 'user'},
            {'label': 'product', 'value': 'product'},
            {'label': 'order', 'value': 'order'}
        ],
        value='user'
    ),
    dcc.Input(id='search-bar', value='', type='text'),
    # dash_table.DataTable(
    #     id='table',
    #     columns=[{"name": i, "id": i} for i in df.columns],
    #     data=df.to_dict('records'),
    # ),
    html.Button('Search', id='search-button'),
    html.Div(id='result-table'),
    html.Div(id='intermediate-value', style={'display': 'none'})
    # generate_table(df)
])

@app.callback(
    Output('intermediate-value', 'children'),
    [dash.dependencies.Input('search-button', 'n_clicks'),
     dash.dependencies.Input('search-option', 'value')],
    [dash.dependencies.State('search-bar', 'value')]
)
def clean_data(n_clicks, type, input_value):
    print(type)
    print(input_value)
    if input_value is not '':
        table = ''
        col = ''
        if type == 'user':
            table = 'customer'
            col = 'user_id'
        elif type == 'product':
            table = 'product'
            col = 'product_id'
        elif type == 'order':
            table = 'purchase'
            col = 'purchase_id'
        sql = """
        select * from {} where {} like '%{}%' limit 100
        """
        conn = connect(host='192.168.43.128', port=10000, user='hadoop', password='sgq199907',
                       auth_mechanism="nosasl",
                       database='default')
        cursor = conn.cursor()
        print(sql.format(table, col, input_value,))
        cursor.execute(sql.format(table, col, input_value,))
        df = pd.DataFrame(as_pandas(cursor))
        cursor.close()
        conn.close()
        return df.to_json(date_format='iso', orient='split')

@app.callback(
    Output(component_id='result-table', component_property='children'),
    [Input('intermediate-value', 'children')]
)
def update_table(jsonified_cleaned_data):
    if(jsonified_cleaned_data is not None):
        df = pd.read_json(jsonified_cleaned_data, orient='split')
        return generate_table(df)

if __name__ == '__main__':
    app.run_server(debug=True)
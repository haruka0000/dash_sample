import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# アプリの宣言
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# HTMLの外観を定義
app.layout = html.Div([
    html.H1(children="App title"),
    # テキストボックス
    dcc.Input(id="input-1", type="text", size=70),
    # 送信ボタン
    html.Button(id="submit-button", children="Submit"),
    # 余白
    html.Div(style={'padding': 10}),
    # 表
    html.Div(id="table-area"),
    # データ格納エリア(非表示)
    html.Div(id='intermediate-value', style={'display': 'none'})
], style={'padding': 50})


## データを格納エリアに格納 ##
@app.callback(
    Output('intermediate-value', 'children'),
    [Input("submit-button", "n_clicks")],
    [State("input-1", "value")]
)
def clean_data(n_clicks, input_text):
    # データ表示　任意のメソッドに置き換える（メソッドの戻り値はpandasデータフレーム型であること）
    df = sample_data(input_text)

    return df.to_json(date_format='iso', orient='split')

## 格納エリアの変化を受けて、テーブルを描画 ##
@app.callback(
    Output("table-area", "children"),
    [Input('intermediate-value', 'children')]
)
def update_table(jsonified_cleaned_data):
    #　格納エリアから取ってきたデータを読み込み
    df = pd.read_json(jsonified_cleaned_data, orient='split')
    
    return dash_table.DataTable(
        id='table-01',
        columns=[{'id': c, 'name': c} for c in df.columns],     # 列名
        data=df.to_dict("rows"),                # データ（行）
        style_table={'width': '100%'},
        style_data={'whiteSpace': 'normal'},
        # 幅等の設定
        # style_cell_conditional=[
        #     {'if': {'column_id': 'order'},
        #         'width': '5%',
        #         'textAlign': 'center',
        #     },
        #     {'if': {'column_id': 'tag'},
        #         'width': '30%',
        #         'textAlign': 'left',
        #     },
        #     {'if': {'column_id': 'text'},
        #         'textAlign': 'left',
        #     },
        #     {'if': {'column_id': 'value'},
        #         'width': '15%',
        #         'textAlign': 'left',
        #     },
        # ],
        content_style='grow',
        # css=[{
        #     'selector': '.dash-cell div.dash-cell-value',
        #     'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        # }],
        # style_header={
        #     'backgroundColor': 'white',
        #     'fontWeight': 'bold'
        # },
    ),


### サンプルデータ表示用
def sample_data(input_text):
    data = [ ["a", 0.9], ["b", 0.8], ["c", 0.7], ["d", 0.6], ["e", 0.5], [input_text, 0.1] ]
    df = pd.DataFrame(data, columns=["tag", "value"])
    return df

if __name__ == "__main__":
    app.run_server(debug=True)

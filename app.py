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
    html.Div([
        # テキストボックス
        dcc.Input(id="input-1", type="text", size=70),
        # テキストボックス
        dcc.Input(id="input-2", type="text", size=20),
    ], style={'display': 'inline-block'}),
    # 送信ボタン
    html.Button(id="submit-button", children="Submit"),
    # 余白
    html.Div(style={'padding': 10}),
    # 表
    html.Div(id="table-area"),
    # グラフ
    dcc.Graph(id="graph"),
    # データ格納エリア(非表示)
    html.Div(id='intermediate-value', style={'display': 'none'})
], style={'padding': 50})


## データを格納エリアに格納 ##
@app.callback(
    Output('intermediate-value', 'children'),
    [Input("submit-button", "n_clicks")],
    [State("input-1", "value"), State("input-2", "value")]
)
def clean_data(n_clicks, input_text, input_text2):
    # データ表示　任意のメソッドに置き換える（メソッドの戻り値はpandasデータフレーム型であること）
    df = sample_data(input_text, float(input_text2))

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
        content_style='grow',
    ),


## 格納エリアの変化を受けて、グラフを描画 ##
@app.callback(
    Output("graph", "figure"),
    [Input('intermediate-value', 'children')]
)
def update_graph(jsonified_cleaned_data):
    df = pd.read_json(jsonified_cleaned_data, orient='split')

    data = {
            "x": list(range(len(df))),
            "y": df["value"].values.tolist(),
            "type": "lines+markers",
            "name": "サンプル０１",
            "text": df["tag"].values.tolist(),
            "hover": "text",
    },
    return {
        "data": data,
        "layout": {
            "title": "サンプル"
        }
    }

### サンプルデータ 表示用 ###
def sample_data(input_text, value):
    data = [ ["a", 0.9], ["b", 0.8], ["c", 0.7], ["d", 0.6], ["e", 0.5], [input_text, value] ]
    df = pd.DataFrame(data, columns=["tag", "value"])
    return df

if __name__ == "__main__":
    app.run_server(debug=True)

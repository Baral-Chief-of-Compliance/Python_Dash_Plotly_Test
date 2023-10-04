from dash import html, Output, Input, State, dcc
from dash_extensions.enrich import (DashProxy, ServersideOutputTransform, MultiplexerTransform)
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
import plotly.express as px
from database.database import start_db

CARD_STYLE = dict(withBorder=True,
                  shadow="sm",
                  radius="md",
                  style={'height': '400px'})


class EncostDash(DashProxy):
    def __init__(self, **kwargs):
        self.app_container = None
        super().__init__(transforms=[ServersideOutputTransform(),
                                     MultiplexerTransform()], **kwargs)

percent_reasons, reason_option, options_for_dropdown, all_records_db = start_db()

app = EncostDash(name=__name__)
pie_chart = px.pie(all_records_db,'reason', hole=.2)
pie_chart.update_layout(
    margin=dict(l=20, r=20, t=0, b=170),
)



def get_layout():
    return html.Div([
        dmc.Paper([
            dmc.Grid([
                dmc.Col([
                    dmc.Card([
                            dmc.TextInput(label='Введите что-нибудь', id='input'),
                            dcc.Dropdown(
                                id="my_dropdown",
                                # options=[
                                #     {"label": "1", "value": "1"},
                                #     {"label": "2", "value": "2"},
                                #     {"label": "3", "value": "3"},
                                #     {"label": "4", "value": "4"}
                                # ],
                                options=options_for_dropdown,
                                multi=True,
                                clearable=True,
                                placeholder="Выберите фильтер",
                                style={
                                    "width": "80%", 
                                    "marginTop": "15px",
                                    "marginBottom": "15px"
                                }
                            ),
                            dmc.Button('Первая кнопка', id='button1'),
                            dmc.Button('Вторая кнопка', id='button2'),
                            html.Div(id='output')
                        ],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                            # html.Div('Верхняя правая карточка'),
                            # html div from wxmaple 
                                # html.Div([
                                #     dcc.Graph(id="graph"),
                                #     dcc.Dropdown(id='names',
                                #         options=reason_option,
                                #         value='day', clearable=False
                                #     ),
                                #     dcc.Dropdown(id='values',
                                #         options=reason_option,
                                #         value='total_bill', clearable=False
                                #     ),
                                # ])
                            # html div from wxmaple 
                            html.Div(
                                dcc.Graph(
                                    figure=pie_chart
                                ),
                                style={
                                    "padingBottom": "200px"
                                }
                            )
                        ],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        html.Div('Нижняя карточка')],
                        **CARD_STYLE)
                ], span=12),
            ], gutter="xl",)
        ])
    ])


app.layout = get_layout()


@app.callback(
    Output('output', 'children'),
    State('input', 'value'),
    Input('button1', 'n_clicks'),
    prevent_initial_call=True,
)
def update_div1(
    value,
    click
):
    if click is None:
        raise PreventUpdate

    return f'Первая кнопка нажата, данные: {value}'


"""app calback from example"""
# @app.callback(
#     Output("graph", "figure"), 
#     Input("names", "value"), 
#     Input("values", "value"))
# def generate_chart(names, values):
#     df = px.data.tips() # replace with your own data source
#     fig = px.pie(df, values=values, names=names, hole=.3)
#     return fig
"""app calback from example"""

# @app.callback(
#         Output(component_id='the_graph', component_property='figure'),
#         [Input(component_id='my_dropdown', component_property='value')]
# )

# def update_graph(my_dropdown):

#     piechart = px.pie(
#         all_records_db,
#         'reason',
#         hole=.2
#     )

#     return piechart


@app.callback(
    Output('output', 'children'),
    State('input', 'value'),
    Input('button2', 'n_clicks'),
    prevent_initial_call=True,
)
def update_div2(
    value,
    click
):
    if click is None:
        raise PreventUpdate

    return f'Вторая кнопка нажата, данные: {value}'


if __name__ == '__main__':
    app.run_server(debug=True)

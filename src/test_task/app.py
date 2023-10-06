from dash import html, Output, Input, State, dcc
from dash_extensions.enrich import (DashProxy, ServersideOutputTransform, MultiplexerTransform)
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import copy
from graphs.graphs import create_pie_graph, create_timeline
import database.database as db


CARD_STYLE = dict(withBorder=True,
                  shadow="sm",
                  radius="md",
                  style={'height': '500px'})


class EncostDash(DashProxy):
    def __init__(self, **kwargs):
        self.app_container = None
        super().__init__(transforms=[ServersideOutputTransform(),
                                     MultiplexerTransform()], **kwargs)


app = EncostDash(name=__name__)


def get_layout():
    return html.Div([
        dmc.Paper([
            dmc.Grid([
                dmc.Col([
                    dmc.Card([
                            html.H1(
                                f"Клиент: {db.client_name}"
                            ),
                            html.H3(
                                f"Сменный день: {db.shift_day}"
                            ),

                            html.H3(
                                f"Точка учета: {db.endpoint_name}"
                            ),

                            html.H3(
                                f"Начало периода: {format(db.state_begin, '%H:%M:%S (%d.%m)')}"
                            ),

                            html.H3(
                                f"Конец периода: {format(db.state_end, '%H:%M:%S (%d.%m)')}"
                            ),

                            dcc.Dropdown(
                                id="filter_dropdown",
                                options=db.options_for_dropdown,
                                multi=True,
                                clearable=True,
                                placeholder="Выберите фильтер",
                                style={
                                    "width": "80%", 
                                    "marginTop": "15px",
                                    "marginBottom": "15px"
                                }
                            ),
                            dmc.Button('Фильтровать', id='filter_button'),
                            html.Div(id='output')
                        ],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                            html.Div(
                                dcc.Graph(
                                    figure=create_pie_graph()
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
                        html.Div(
                            dcc.Graph(
                                id="time_line_graph",
                                figure=create_timeline(db.color_map),
                                
                                
                            )
                        )
                        
                        ],
                        **CARD_STYLE)
                ], span=12),
            ], gutter="xl",)
        ])
    ])


app.layout = get_layout()



@app.callback(
    Output(component_id='time_line_graph', component_property='figure'),
    State(component_id='filter_dropdown', component_property='value'),
    Input(component_id='filter_button', component_property='n_clicks'),
    prevent_initial_call=True,
)

def show_value(value, click):
    if click is None:
        raise PreventUpdate
    
    changed_unselected_map = copy.deepcopy(db.unselected_map)
    for v in value:
        if v in changed_unselected_map:
            changed_unselected_map[v] = db.color_map[v]

    fig_gant = create_timeline(changed_unselected_map)
    return fig_gant

if __name__ == '__main__':
    app.run_server(debug=True)

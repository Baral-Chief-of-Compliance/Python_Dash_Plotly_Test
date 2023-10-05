from dash import html, Output, Input, State, dcc
from dash_extensions.enrich import (DashProxy, ServersideOutputTransform, MultiplexerTransform)
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
import plotly.express as px
from database.database import start_db
import pandas as pd


CARD_STYLE = dict(withBorder=True,
                  shadow="sm",
                  radius="md",
                  style={'height': '400px'})


class EncostDash(DashProxy):
    def __init__(self, **kwargs):
        self.app_container = None
        super().__init__(transforms=[ServersideOutputTransform(),
                                     MultiplexerTransform()], **kwargs)

percent_reasons, reason_option, options_for_dropdown, all_records_db, color_map, unselected_map = start_db()

app = EncostDash(name=__name__)
pie_chart = px.pie(all_records_db,'reason', hole=.2, color="reason", color_discrete_map  = color_map)
pie_chart.update_layout(
    margin=dict(l=20, r=20, t=0, b=170),
)

fig_gant = px.timeline(
    all_records_db, 
    x_start="state_begin", 
    x_end="state_end", 
    y="endpoint_name", 
    color='reason', 
    color_discrete_map = color_map,
    custom_data=[
        'state',
        'reason',
        'state_begin',
        'duration_min',
        'calendar_day',
        'period_name',
        'operator'
    ]
)

fig_gant.update_traces(
    hoverlabel=dict(
        bgcolor = ['white']
    ),
    hovertemplate="<br>".join([
        'Состояние - <b>%{customdata[0]}</b>',
        'Причина - <b>%{customdata[1]}</b>',
        'Начало - <b>%{customdata[2]| %H:%M:%S}</b> (%{customdata[2]|%d.%m})',
        'Длительность - <b>%{customdata[3]:,.2f}</b> мин.<br><br>',
        'Сменный день - <b>%{customdata[4]}</b>',
        'Смена - <b>%{customdata[5]}</b>',
        'Оператор - <b>%{customdata[6]}</b>'
    ])
)

fig_gant.update_layout(
    title_text='График состояний',
    xaxis_title="",
    yaxis_title="",
    showlegend=False
)





def get_layout():
    return html.Div([
        dmc.Paper([
            dmc.Grid([
                dmc.Col([
                    dmc.Card([
                            dcc.Dropdown(
                                id="filter_dropdown",
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
                            dmc.Button('Фильтровать', id='filter_button'),
                            html.Div(id='output')
                        ],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
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
                        html.Div(
                            dcc.Graph(
                                id="time_line_graph",
                                figure=fig_gant,
                                
                                
                            )
                        )
                        
                        ],
                        **CARD_STYLE)
                ], span=12),
            ], gutter="xl",)
        ])
    ])


app.layout = get_layout()




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



# @app.callback(
#     Output(component_id='time_line_graph', component_property='figure'),
#     [Input(component_id='filter_dropdown', component_property='value')]
# )

# def highlight_part_graph(filter_dropdown):

#     piechart = px.pie(
#         all_records_db,
#         'reason',
#         hole=.2
#     )

#     return piechart


@app.callback(
    Output(component_id='time_line_graph', component_property='figure'),
    State(component_id='filter_dropdown', component_property='value'),
    Input(component_id='filter_button', component_property='n_clicks'),
    prevent_initial_call=True,
)

def show_value(value, click):
    if click is None:
        raise PreventUpdate
    
    changed_unselected_map = unselected_map
    print(value)
    print("\n\n")
    print(changed_unselected_map)
    print("\n\n")
    print(unselected_map)
    for v in value:
        if v in changed_unselected_map:
            changed_unselected_map[v] = color_map[v]

    fig_gant = px.timeline(
    all_records_db, 
    x_start="state_begin", 
    x_end="state_end", 
    y="endpoint_name", 
    color='reason', 
    color_discrete_map = changed_unselected_map,
    custom_data=[
        'state',
        'reason',
        'state_begin',
        'duration_min',
        'calendar_day',
        'period_name',
        'operator'
    ]
)
    return fig_gant

if __name__ == '__main__':
    app.run_server(debug=True)

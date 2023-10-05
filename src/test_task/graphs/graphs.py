import plotly.express as px
import database.database as db


def create_pie_graph():
    pie_chart = px.pie(db.all_records_db, 'reason', hole=.2, color='reason', color_discrete_map=db.color_map)
    pie_chart.update_layout(
        margin=dict(l=20, r=20, t=0, b=170),
    )

    return pie_chart


def create_timeline(color_map):
    fig_gant = px.timeline(
        db.all_records_db, 
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

    return fig_gant
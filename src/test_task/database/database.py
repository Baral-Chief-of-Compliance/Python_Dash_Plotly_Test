import pandas as ps
import sqlite3
from colors.colors import make_color_lighter
from datetime import datetime


con = sqlite3.connect("testDB.db")


def get_all_records():
    all_records_db = ps.read_sql("select * from sources", con)

    return all_records_db


def prepare_data():
    reason_option = []
    options_for_dropdown = []
    color_map = {}
    unselected_map = {}

    all_reasons = ps.read_sql("select distinct sources.reason, sources.color from sources", con)
   

    for index, row in all_reasons.iterrows():
        reason_option.append(row['reason'])
        options_for_dropdown.append({"label": row['reason'], "value": row['reason']})
        color_map[row['reason']] = row['color']
        unselected_map[row['reason']] = make_color_lighter(row['color'])
        
    return reason_option, options_for_dropdown, color_map, unselected_map



def get_client_name():
    client = ps.read_sql("select distinct sources.client_name as client_name from sources", con)
    return client['client_name'][0]


def get_boarder_period():
    state_begin = ps.read_sql("select min(sources.state_begin) as state_begin from sources", con)
    state_end = ps.read_sql("select max(sources.state_end) as state_end from sources", con)
    state_begin['state_begin'] = ps.to_datetime(state_begin.state_begin, format='%Y-%m-%d %H:%M:%S.%f')
    state_end['state_end'] = ps.to_datetime(state_end.state_end, format='%Y-%m-%d %H:%M:%S.%f')
    return state_begin['state_begin'][0], state_end['state_end'][0]


def get_shift_day():
    shift_day = ps.read_sql("select distinct sources.shift_day as shift_day from sources", con)
    return shift_day['shift_day'][0]


def get_endpoint_inf():
    endpoint_inf = ps.read_sql("select distinct sources.endpoint_name as endpoint_name from sources", con)
    return endpoint_inf['endpoint_name'][0]


all_records_db = get_all_records()

reason_option, options_for_dropdown, color_map, unselected_map = prepare_data()

client_name = get_client_name()
shift_day = get_shift_day()
endpoint_name = get_endpoint_inf()
state_begin, state_end = get_boarder_period()





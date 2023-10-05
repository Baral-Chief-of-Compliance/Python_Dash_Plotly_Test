import pandas as ps
import sqlite3
from colors.colors import make_color_lighter


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
        count_reson = ps.read_sql(f"select count(sources.reason) as county from sources where sources.reason = ?", con, params=(row['reason'], ))
        reason_option.append(row['reason'])
        options_for_dropdown.append({"label": row['reason'], "value": row['reason']})
        color_map[row['reason']] = row['color']
        unselected_map[row['reason']] = make_color_lighter(row['color'])
        
    return reason_option, options_for_dropdown, color_map, unselected_map


all_records_db = get_all_records()
reason_option, options_for_dropdown, color_map, unselected_map = prepare_data()
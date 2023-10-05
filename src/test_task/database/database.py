import pandas as ps
import sqlite3

def start_db():
    percent_reasons = {}
    reason_option = []
    options_for_dropdown = []
    color_map = {}
    unselected_map = {}

    con = sqlite3.connect("testDB.db")
    all_records_db = ps.read_sql("select * from sources", con)
    count_all_records = ps.read_sql("select count(sources.reason) as county from sources", con)
    count_all_records = count_all_records['county'][0] 



    all_state = ps.read_sql("select distinct sources.state from sources", con)

    all_reasons = ps.read_sql("select distinct sources.reason, sources.color from sources", con)
   

    for index, row in all_reasons.iterrows():
        count_reson = ps.read_sql(f"select count(sources.reason) as county from sources where sources.reason = ?", con, params=(row['reason'], ))
        reason_option.append(row['reason'])
        percent_reasons[row['reason']] = (count_reson['county'][0] / count_all_records) * 100
        options_for_dropdown.append({"label": row['reason'], "value": row['reason']})
        color_map[row['reason']] = row['color']
        unselected_map[row['reason']] = "#696969"

    return percent_reasons, reason_option, options_for_dropdown, all_records_db, color_map, unselected_map
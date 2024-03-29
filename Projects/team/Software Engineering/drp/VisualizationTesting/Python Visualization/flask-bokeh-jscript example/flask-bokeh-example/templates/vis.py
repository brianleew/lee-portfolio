import json

import bokeh
from bokeh.plotting import figure
from bokeh.embed import json_item

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool, HoverTool

import pandas as pd
import numpy as np

import db.py

def bokehMeter(meter_name):

    conn = connect_db()

    query = "select meter_data.value as power, meter_data.start_time as start from meter_data where meter_data.meter_name = '{}';".format(meter_name)
    GetSQLTest = pd.read_sql_query(query,conn)

    query = "select * from meter_prediction where meter_prediction.meter_name = '{}';".format(meter_name)
    prediction_data = pd.read_sql_query(query,conn)

    GetSQLTest["start"] = pd.to_datetime(GetSQLTest["start"])

    prediction_data["start"] = pd.to_datetime(prediction_data["start_time"])
    prediction_data = prediction_data.drop(["meter_name","start_time","end_time"],axis = 1)
    print(prediction_data)

    dates =pd.date_range('2021-03-21 00:00:00', '2021-09-27 23:30:00', freq = '30T')
    
    merge =  pd.DataFrame(dates,columns=["dates"]).merge(GetSQLTest,how = "left", left_on = "dates", right_on = "start")
    print(merge)
    merge2 = merge.merge(prediction_data,how = "left", left_on = "dates", right_on = "start")
    print(merge2.dropna())
    source = ColumnDataSource(data=dict(date=merge2["dates"], close=merge2['power'],open = merge2["meter_value"]))
    
    p = figure(height=300, width=800, tools="xpan", toolbar_location=None,
            x_axis_type="datetime", x_axis_location="above",
            background_fill_color="#efefef", x_range=(dates[1500], dates[2500]),sizing_mode="scale_both")

    p1 = p.line('date', 'close', source=source)
    p2 = p.line("date","open",source = source,line_color = "red")
    #p3 = p.circle("date",'close',source=source, size = 2, color = "blue", line_color = "blue")
    #p4 = p.triangle("date","open",source = source, size = 2, color = "red", line_color = "red")
    
    hover_tool = HoverTool(renderers=[p1], tooltips=[('power',"@close"),('prediction',"@open")],mode='vline')
    p.add_tools(hover_tool)
    p.toolbar.active_multi = "auto"

    p.yaxis.axis_label = 'kw'

    select = figure(title="Drag the middle and edges of the selection box to change the range above",
                    height=130, width=800, y_range=p.y_range,
                    x_axis_type="datetime", y_axis_type=None,
                    tools="", toolbar_location=None, background_fill_color="#efefef",sizing_mode="scale_both")

    range_tool = RangeTool(x_range=p.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    
    select.line('date', 'close', source=source)
    select.line("date","open", source=source)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    
    select.toolbar.active_multi = 'auto'

    layout = column(p, select,sizing_mode = "scale_both")
    return json.dumps(json_item(layout))

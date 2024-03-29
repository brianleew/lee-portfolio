import json
import math

from bokeh.plotting import figure, gmap
from bokeh.embed import json_item

from bokeh.layouts import column, row
from bokeh.models import (ColumnDataSource, RangeTool, HoverTool,Legend,LegendItem,
                          CustomJS, Select, Button, TabPanel, Tabs, Spacer,
                          AjaxDataSource,Plot,Text,Title,GMapOptions)


from bokeh.transform import cumsum

from statsmodels.tsa.stattools import pacf, acf, adfuller

import pandas as pd
import numpy as np

from .db import connect_db
from .users import get_user_org, linked_meter_ids
from .session import get_session_data
from .config import load_config

# ------ ALL FUNCTIONS TO RETRIEVE DATA FROM THE DATABASE ----------
def get_meter_data_private(session_id,meter_id):
  conn = connect_db()
  meter_data = pd.read_sql("""SELECT start_time, meter_value, prediction_value
                            FROM meter_data
                            WHERE meter_data.meter_id = %(meter_id)s
                           ;""", conn,  params={"meter_id" : meter_id})
  conn.close()
  ranges = pd.DataFrame({"start_time":pd.date_range(meter_data['start_time'].values[0], meter_data['start_time'].values[-1], freq = '30T')})
  meter_data = pd.merge(ranges, meter_data,  how='left', left_on=['start_time'], right_on = ['start_time'])
  return meter_data

def get_meter_data(session_id,meter_id):
  return get_meter_data_private(session_id=session_id,meter_id=meter_id).to_json(orient="table")

def get_pie_data_private(session_id, meter_id):
  conn = connect_db()
  pie_part = pd.read_sql("""select (p/t) as participation,(1-p/t)as not_participation
                            from (select count(delta_value) as t
                                from meter_data
                                where meter_id = %(meter_id)s
                                group by meter_id) as t
                            join (select count(delta_value) as p
                                from meter_data
                                where meter_id = %(meter_id)s and delta_value > 0
                                group by meter_id) as p;""", conn,  params={"meter_id" : meter_id})
  conn.close()
  pi = math.pi
  pp = pie_part["participation"][0]
  not_p = pie_part["not_participation"][0]
  pa = pp*2*pi
  not_pa = not_p * 2 * pi
  pp = str(pp*100) + "%"
  not_p = str(not_p*100) + "%"
  par = [pp,not_p]
  angle = [pa,not_pa]
  names =["Participated","Not Participated"]
  color = ["#00ff00","#ff0000"]
  pie_data = pd.DataFrame({"name":names,
        "percent":par,
        "angle":angle,
        "color":color,})

  return pie_data

def get_pie_data(session_id, meter_id):
  return get_pie_data_private(session_id, meter_id).to_json(orient="table")

# get the total data as a pandas dataframe
# used to call in the above python function
# without having to convert it to json
def get_total_data_private(session_id, meter_id):
  conn = connect_db()
  total_data = pd.read_sql("""SELECT sum(delta_value*1) as savings
                              FROM meter_data
                              WHERE meter_id = %(meter_id)s
                           ;""", conn,  params={"meter_id" : meter_id})
  conn.close()
  return total_data

def get_total_data(session_id, meter_id):
  return get_total_data_private(session_id, meter_id).to_json(orient="columns")

def get_event_data_private():
  conn = connect_db()
  meter_data = pd.read_sql("""SELECT distinct start_time, end_time
                            FROM meter_data
                            ;""", conn)
  ranges = pd.DataFrame({"start_time":pd.date_range(meter_data['start_time'].values[0], meter_data['start_time'].values[-1], freq = '30T')})
  meter_data = pd.merge(ranges, meter_data,  how='left', left_on=['start_time'], right_on = ['start_time'])
  event_data = pd.read_sql("""select distinct start_time, end_time
                            from drp_periods;""", conn)
  conn.close()
  d1 = pd.merge(meter_data["start_time"], event_data,  how='left', left_on=['start_time'], right_on = ['start_time']).dropna()
  d2 = pd.merge(meter_data["end_time"], event_data,  how='left', left_on=['end_time'], right_on = ['end_time']).dropna()
  d1.reset_index(inplace = True)
  d1["start_index"] = d1["index"]
  d1.drop(["index"], axis = 1, inplace = True)
  d2.reset_index(inplace = True)
  d2["end_index"] = d2["index"]
  d2.drop(["index"], axis = 1, inplace = True)
  drp = pd.merge(d1, d2,  how='left', left_on=['start_time',"end_time"], right_on = ['start_time',"end_time"]).dropna()
  return drp
def get_geo_data():
  conn = connect_db()
  geo_data =  pd.read_sql("""select x.meter_id,participation,delta_value
from(	select distinct *
	from meter_map
	where entity_id != 1
	order by entity_id) as y
left join (	select t.meter_id,(p/t) as participation,(1-p/t)as not_participation
			from (	select meter_id,count(delta_value) as t
					from meter_data
					group by meter_id) as t
			left join (	select meter_id,count(delta_value) as p
						from meter_data
						where delta_value > 0
						group by meter_id) as p
			on t.meter_id = p.meter_id) as x
on x.meter_id = y.meter_id
left join (select meter_id, sum(delta_value) as delta_value
			from meter_data
            group by meter_id) as z
on z.meter_id = x.meter_id;""", conn)
  conn.close()
  return geo_data
def check_stationarity(series, verbose = False):

      result = adfuller(series.values)

      if verbose:
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        print('Critical Values:')
        for key, value in result[4].items():
            print('\t%s: %.3f' % (key, value))

      if (result[1] <= 0.05) & (result[4]['5%'] > result[0]):
          if verbose: print("\u001b[32mStationary\u001b[0m")
          return True
      else:
          if verbose: print("\x1b[31mNon-stationary\x1b[0m")
          return False


def get_acf_data_private(session_id, meter_id):
  meter_data = get_meter_data_private(session_id,meter_id)
  data = meter_data["meter_value"].dropna()
  acf_data = pd.DataFrame(dict(
                  x = pd.Series(range(1, len(data)+1), dtype = float),
                  y = acf(data,nlags = len(data))))


  return acf_data

def get_acf_data(session_id, meter_id):
   return get_acf_data_private(session_id, meter_id).to_json(orient="table")

def get_pacf_data_private(session_id, meter_id):

  meter_data = get_meter_data_private(session_id,meter_id)
  data = meter_data["meter_value"].dropna()
  if(not(check_stationarity(pd.Series(data)))):
    data = data.diff().fillna(0)

  lag_pacf = pacf(data,method="ols")
  y1 = pd.DataFrame(lag_pacf).values.squeeze()
  x1 = [x for x in range(len(lag_pacf))]
  x2= x1
  y2 = [0] * len(lag_pacf)
  seg = {"y1":y1,
        "y2":y2,
        "x1":x1,
        "x2":x2
  }

  return pd.DataFrame(seg)

def get_pacf_data(session_id, meter_id):
   return get_pacf_data_private(session_id, meter_id).to_json(orient="table")

def significance(series):
      n = len(series)
      z95 = 1.959963984540054 / np.sqrt(n)
      z99 = 2.5758293035489004 / np.sqrt(n)
      return(z95,z99)

def get_sig_data_private(session_id,meter_id):
  meter_data = get_meter_data_private(session_id,meter_id)
  data = meter_data["meter_value"].dropna()
  z95, z99 = significance(data)
  sig = dict(y=[0, z99,z99*-1,z95,z95*-1], line_width=[1,2,2,2,2], line_color=["black","gray","gray","gray","gray"], line_dash = ["solid","dashed","dashed","solid","solid"])

  return pd.DataFrame(sig)

def get_sig_data(session_id,meter_id):
   return get_sig_data_private(session_id,meter_id).to_json(orient="table")

def get_org_data(session_id,meter_id):
  conn = connect_db()
  olist = pd.read_sql("""select org_id,org_name
                          from organizations
                          where org_id != 1;""", conn)

  ml = {}
  for i,row in olist.iterrows():
    ml[row["org_name"]] =  pd.read_sql("""select meter_id
                                          from meter_map
                                          where entity_id = %(e)s
                           ;""", conn,  params={"e" : row["org_id"]})["meter_id"].values
  conn.close()
  return ml

# --------- The Creation of the bokeh layout --------------
def data_source_admin(session_id,meter_id,org_id):
#----------------------------------------------------------
#def get_line_source(session_id,meter_id)
  meter_data = get_meter_data_private(session_id=session_id,meter_id=meter_id)

  adapter = CustomJS(code="""
      const result = {start_time:[],meter_value: [], prediction_value: []}
      const {data} = cb_data.response
      data.forEach((meter) => {
                      if (meter.prediction_value === null) {
                        result.prediction_value.push(NaN); // Use NaN for null values
                      } else {
                        result.prediction_value.push(meter.prediction_value); // Keep non-null values as they are
                      }
                      if (meter.meter_value === null) {
                        result.meter_value.push(NaN); // Use NaN for null values
                      } else {
                        result.meter_value.push(meter.meter_value); // Keep non-null values as they are
                      }
                     result.start_time.push(Date.parse(meter.start_time));
                     //result.prediction_value.push(meter.prediction_value);
});
      return result
    """)

  line_source = AjaxDataSource(data_url='/api/vis/meter_data/{m}/'.format(m=meter_id),
                        polling_interval=1000, adapter=adapter, method = 'GET', mode='replace')



  line_source.data = dict(start_time=meter_data["start_time"], meter_value=meter_data["meter_value"], prediction_value = meter_data["prediction_value"])
  line = figure(height=300, width=1300, tools="xpan", toolbar_location=None,
            x_axis_type="datetime", x_axis_location="above",x_range=(line_source.data["start_time"].values[int(len(line_source.data["start_time"])* .888888888)], line_source.data["start_time"].values[-1]),
            background_fill_color="#efefef",sizing_mode="fixed")

  line_source.js_on_change("data", CustomJS(args=dict(line = line),code="""
                                    let values = cb_obj.data["meter_value"].filter(value => Number.isFinite(value));
                                    //console.log(values)
                                    let maxValue = Math.max.apply(null, values);
                                    let minValue = Math.min.apply(null,values);
                                    //console.log(maxValue + (maxValue * .1));
                                    //console.log(minValue - (minValue * .1));
                                    line.y_range.start = minValue;
                                    line.y_range.end = maxValue;
    """))

  prediction_circle = line.circle("start_time", "prediction_value", size=5,
              fill_color="red", alpha=0, line_color=None,
              hover_fill_color="red", hover_alpha=0.5,
              hover_line_color="white",source = line_source)

  meter_circle = line.circle("start_time", "meter_value", size=5,
              fill_color="blue", alpha=0, line_color=None,
              hover_fill_color="blue", hover_alpha=0.5,
              hover_line_color="white",source = line_source)

  p1 = line.line('start_time', 'meter_value', source=line_source)
  p2 = line.line("start_time","prediction_value",source = line_source,line_color ="red")

  # Create a HoverTool for p1
  hover_tool_p1 = HoverTool(renderers=[p1], tooltips=[('power', '@meter_value'),('prediction','@prediction_value')], mode='vline')
  # Create a HoverTool for p2
  hover_tool_p2 = HoverTool(renderers=[prediction_circle,meter_circle], mode='vline', tooltips = None)

  # Add the HoverTools to the figure
  line.add_tools(hover_tool_p1, hover_tool_p2)
  line.toolbar.active_multi = "auto"

  line.yaxis.axis_label = 'kw'

  range_line = figure(title="Drag the middle and edges of the selection box to change the range above",
                    height=130, width=1300, y_range=line.y_range,
                    x_axis_type="datetime", y_axis_type=None,
                    tools="", toolbar_location=None, background_fill_color="#efefef",sizing_mode="fixed")

  range_tool = RangeTool(x_range=line.x_range)
  range_tool.overlay.fill_color = "navy"
  range_tool.overlay.fill_alpha = 0.2

  s1 = range_line.line('start_time', 'meter_value', source=line_source)
  s2 = range_line.line("start_time","prediction_value", source=line_source, line_color = "red")
  range_line.ygrid.grid_line_color = None
  range_line.add_tools(range_tool)
  range_line.toolbar.active_multi = 'auto'

  legend_figure = figure(
      title=None, width=300, height=126,
      min_border=0, toolbar_location=None,sizing_mode="fixed",margin = (5,10,10,10))


  legend_figure.xaxis.visible = False
  legend_figure.yaxis.visible = False

  legend_figure.grid.grid_line_color = (0,0,0,0)
  legend_figure.outline_line_color = (0,0,0,0)
  legend_figure.background_fill_color = "#EBEBEB"
  legend_figure.border_fill_color = "#EBEBEB"
  legend_figure.min_border = 0

  l1 = legend_figure.line(x = 1, y = 1,visible = False,line_width= 10)
  l2 = legend_figure.line(x = 1,y = 1, line_color = "red", visible = False, line_width = 10)
  legend = Legend(items = [LegendItem(label = "Meter Data",renderers = [p1,s1,l1,meter_circle]), LegendItem(label = "Prediction Data", renderers = [p2,s2,l2,prediction_circle])],location = "center")
  legend.click_policy = "mute"
  legend.border_line_color = None
  legend.background_fill_color = "#EBEBEB"
  legend.glyph_width = 50
  legend.glyph_height = 20
  legend.label_width = 75
  legend.label_height = 20
  legend.label_text_font_size = "20px"
  legend.label_text_font = "helvetica"
  legend_figure.add_layout(legend,place="center")



  pie_data = get_pie_data_private(session_id,meter_id)

  pie_data = dict(name=pie_data["name"],
        percent=pie_data["percent"],
        angle=pie_data["angle"],
        color=pie_data["color"],)
  adapt_pie = CustomJS(code="""
      const result = {name:[],percent: [], angle: [],color:[]}
      const {data} = cb_data.response
      data.forEach((meter) => {
                    result.name.push(meter.name);
                    result.percent.push(meter.percent);
                    result.angle.push(meter.angle);
                    result.color.push(meter.color);
});
      return result
    """)

  pie_source = AjaxDataSource(data_url='/api/vis/pie_data/{m}/'.format(m=meter_id),
                        polling_interval=1000, adapter=adapt_pie, method = 'GET', mode='replace')

  pie_source.data = pie_data
  pie = figure(height=126,width = 200, toolbar_location=None,
            tools="hover", tooltips="@name:@percent", x_range=(-0.5, 1.0))

  pie.annular_wedge(x=.25, y=1,inner_radius = 0, outer_radius=0.45,
          start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
          line_color="white", fill_color='color', source=pie_source)

  pie.axis.axis_label = None
  pie.axis.visible = False
  pie.grid.grid_line_color = None
  pie.outline_line_color = None
  pie.background_fill_color = None
  pie.border_fill_color = None

  text = "$" + str(get_total_data_private(session_id, meter_id)["savings"][0])

  adapt_text = CustomJS(code="""
      const result = {x:[],y:[],text:[]}
      const {savings} = cb_data.response
      result.text.push("$" + savings[0].toString());
      result.x.push(1);
      result.y.push(1);
      return result
    """)

  text_source = AjaxDataSource(data_url='/api/vis/total_data/{m}/'.format(m=meter_id),
                        polling_interval=1000, adapter=adapt_text, method = 'GET', mode='replace')

  text_source.data = dict(x=[1], y=[1], text=[text])

  total_card = Plot(
      title=None, width=300, height=126,
      min_border=0, toolbar_location=None,sizing_mode = "inherit", margin = (5,10,10,10))


  text_glyph = Text(x="x", y="y", text="text", text_color="#000000")
  text_glyph.text_font_size = "3vmax"
  text_glyph.text_align = "center"
  text_glyph.y_offset = 25
  #text_glyph.text_font = "helvetica"
  #glyph.text_
  total_card.add_glyph(text_source, text_glyph)

  total_card.xaxis.visible = False

  # change some things about the y-axis
  total_card.yaxis.visible = False
  caption = "Total Savings"
  total_card.grid.grid_line_color = (0,0,0,0)
  total_card.outline_line_color = None
  total_card.background_fill_color = "#EBEBEB"
  total_card.border_fill_color = "#EBEBEB"
  total_card.add_layout(Title(text=caption, align="center"),"below")

  fig = column(line,range_line)
  demand_days = get_event_data_private()
  demand_days["display_titles"] = ["{s} - {e}".format(s= demand_days["start_time"][i],e = demand_days["end_time"][i]) for i in range(0,demand_days.shape[0])]
  demand_days_list = list(pd.concat([demand_days["display_titles"][::-1],pd.Series(["All Meter Data"])])[::-1])

  x_ranges = demand_days.to_dict()
  event_select = Select(title="Select Response Date:", value="All Meter Data", options=demand_days_list)
  event_select.js_on_change("value", CustomJS(args=dict(figure = fig, x_ranges = x_ranges),code="""
        ////console.log('select: value=' + this.value)
        //console.log(figure.children[0].renderers[0].data_source.data["start_time"].length)

        if (this.value == "All Meter Data"){
          figure.children[0].x_range.start = figure.children[0].renderers[0].data_source.data["start_time"][figure.children[0].renderers[0].data_source.data["start_time"].length - 1440];
          figure.children[0].x_range.end = figure.children[0].renderers[0].data_source.data["start_time"][figure.children[0].renderers[0].data_source.data["start_time"].length-1];
          figure.children[1].visible = true;
          figure.children[0].height = 300;
        }
        else{
          ////console.log(x_ranges["display_titles"].size)
            x_ranges["display_titles"].forEach((values, keys) => {
              if (this.value == values){
                figure.children[0].x_range.start = figure.children[0].renderers[0].data_source.data["start_time"][x_ranges["start_index"].get(keys)];
                figure.children[0].x_range.end = figure.children[0].renderers[0].data_source.data["start_time"][x_ranges["end_index"].get(keys)];
            }
            //console.log(values, keys);
            });
          figure.children[1].visible = false;
          figure.children[0].height = 430;
        }
    """))
  if not(org_id):
    return row(column(row(legend_figure,row(total_card),pie,column(event_select)), fig))
  elif org_id != 1:

    gdict = get_org_data(session_id,meter_id)
    olist = list(gdict.keys())
    # session_data, _ = get_session_data(session_id)
    # mlist = linked_meter_ids(session_data['account_id'])
    mlist = list(gdict[olist[0]])
    options = [str(i) for i in mlist]
    meter_customer_select = Select(title="Select Meter:", value=options[0], options=options)
    meter_customer_select.js_on_change("value", CustomJS(args=dict(line_source = line_source, pie_source = pie_source,text_source = text_source),code="""
                                      line_source.data_url = '/api/vis/meter_data/' + this.value + "/"
                                      pie_source.data_url = '/api/vis/pie_data/' + this.value + "/"
                                      text_source.data_url = '/api/vis/total_data/' + this.value + "/"
    """))
    return row(column(row(legend_figure,row(total_card),pie,column(meter_customer_select,event_select)), fig))
#--------------------------------------------------
#--------------------------------------------------
  else:
    adapt_sig = CustomJS(code="""
        const result = {y: [], line_width: [], line_color: [], line_dash: []}
        const {data} = cb_data.response
        data.forEach((meter) => {
                        result.y.push(meter.y);
                        result.line_width.push(meter.line_width);
                        result.line_color.push(meter.line_color);
                        result.line_dash.push(meter.line_dash);
  });
        return result
      """)

    source_sig = AjaxDataSource(data_url='/api/vis/sig_data/{m}/'.format(m=meter_id),
                          polling_interval=1000, adapter=adapt_sig, method = 'GET', mode='replace')
    sig_data = get_sig_data_private(session_id,meter_id)
    source_sig.data = dict(y=sig_data["y"],line_width = sig_data["line_width"],line_color=sig_data["line_color"], line_dash = sig_data["line_color"])

    adapt_acf = CustomJS(code="""
        const result = {x:[],y: []}
        const {data} = cb_data.response
        data.forEach((meter) => {
                        result.x.push(meter.x);
                        result.y.push(meter.y);
  });
        return result
      """)

    source_acf = AjaxDataSource(data_url='/api/vis/acf_data/{m}/'.format(m=meter_id),
                          polling_interval=1000, adapter=adapt_acf, method = 'GET', mode='replace')
    acf_data = get_acf_data_private(session_id,meter_id)
    source_acf.data = dict(x = acf_data["x"], y = acf_data["y"])
    acf = figure(title='Time Series Auto-Correlation', width=1300, toolbar_location=None,
                  height=500, x_axis_label="Lag", y_axis_label="Autocorrelation")
    acf.line("x", "y", line_width=2, source = source_acf)
    acf.hspan(y="y",line_width="line_width", line_color="line_color", line_dash ="line_dash",source = source_sig)
  #-------------------------------------------------------------------------------
    adapt_pacf = CustomJS(code="""
        const result = {x1:[],x2: [], y1: [],y2: []}
        const {data} = cb_data.response
        data.forEach((meter) => {
                          result.x1.push(meter.x1);
                          result.x2.push(meter.x2);
                          result.y1.push(meter.y1);
                          result.y2.push(meter.y2);
                      //result.prediction_value.push(meter.prediction_value);
  });
        return result
      """)

    source_pacf = AjaxDataSource(data_url='/api/vis/pacf_data/{m}/'.format(m=meter_id),
                          polling_interval=1000, adapter=adapt_pacf, method = 'GET', mode='replace')
    pacf_data = get_pacf_data_private(session_id,meter_id)
    source_pacf.data = dict(x1 = pacf_data["x1"],x2 = pacf_data["x2"],y1 = pacf_data["y1"],y2 = pacf_data["y2"])
    pacf = figure(title='Time Series Partial Auto-Correlation', toolbar_location=None, width=1300,
                  height=500, x_axis_label="Lag", y_axis_label="Partial Autocorrelation")
    pacf.segment(x0="x1", y0="y1", x1="x2",
          y1="y2", line_width=2, source = source_pacf)
    pacf.circle(source = source_pacf, x="x1", y="y1", size = 4)

    pacf.hspan(y="y",line_width="line_width", line_color="line_color", line_dash ="line_dash",source = source_sig)
    #------------------------------------------------------
  #-----------------------------------------
    gdict = get_org_data(session_id,meter_id)
    olist = list(gdict.keys())
    #session_data, _ = get_session_data(session_id)
    # mlist = linked_meter_ids(session_data['account_id'])
    mlist = list(gdict[olist[0]])
    options = [str(i) for i in mlist]
    meter_select = Select(title="Select Meter:", value=options[0], options=options)
    meter_select.js_on_change("value", CustomJS(args=dict(line_source = line_source, pie_source = pie_source,text_source = text_source, source_sig = source_sig, source_acf = source_acf, source_pacf = source_pacf),code="""
                                      line_source.data_url = '/api/vis/meter_data/' + this.value + "/"
                                      pie_source.data_url = '/api/vis/pie_data/' + this.value + "/"
                                      text_source.data_url = '/api/vis/total_data/' + this.value + "/"
                                      source_sig.data_url = '/api/vis/sig_data/' + this.value + "/"
                                      source_acf.data_url = '/api/vis/acf_data/' + this.value + "/"
                                      source_pacf.data_url = '/api/vis/pacf_data/' + this.value + "/"
    """))

    org_select = Select(title = "Select Organization: ", value = olist[0], options = olist)
    org_select.js_on_change("value",CustomJS(args=dict(meter_select = meter_select, gdict = gdict),code="""
                                      let options = {options: []}
                                      gdict[this.value].forEach((meter) => {
                                          options.options.push(meter.toString());
                                      });
                                      meter_select.options = options["options"]
                                      meter_select.value = meter_select.options[0]

    """))
    #----------------------------------------
    #------------------------------------------

    geo_data = get_geo_data()
    map_options = GMapOptions(lat=36.175824, lng=-85.504218, map_type="satellite", zoom=17)

    TOOLTIPS = """
    <body  style="background-color:rgba(0,0,0,0);">
    <div class="card" style="width: 300px; height: 390px;">
      <img src="@imgs" alt="Avatar" style="width: 100%; border-radius: 5px; margin-bottom: 5px;">
      <div class="title" style="text-align: center; border-radius: 5px;background-color: @color;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);">
        <h2 style="margin: 5px 0; font-size: 2vw; white-space: wrap;color: @font;"><b>@name</b></h2>
    </div>
      <div class="columns" style="display: flex;">
        <div class="column" style="padding: 0 10px; text-align: left; flex: 1; border-radius: 5px;background-color: @color;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);margin-right: 2px;">
          <p style = "color: @font;"><b>Rank: $index</b></p>
          <p style = "color: @font;";><b>Savings: @delta</b></p>
        </div>
        <div class="column" style="padding: 0 10px; text-align: left; flex: 1; border-radius: 5px;background-color: @color;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);margin-left: 2px;">
          <p style = "color: @font;"><b>Meter: @meter_id</b></p>
          <p style = "color: @font;"><b>Participation: @rate</b></p>
        </div>
      </div>
    </div>
    </body>

    """

    p = gmap("AIzaSyCry4EYsY4D60_F4oOneAnKZF2J0xCb_-4", map_options, title="Tennessee Tech",tools = ["pan"], width= 1300,toolbar_location=None )
    legend = Legend(click_policy = "hide")
    p.add_layout(legend,"right")

    md = pd.DataFrame(dict(lat= [
        36.172462,    36.172550,    36.172984,    36.17239,    36.172327,    36.172281,    36.172943,    36.172981,
        36.17217,    36.172829,    36.172652,    36.174239,    36.174674,    36.17365,    36.174473,    36.174555,
        36.176519,    36.175244,    36.175848,    36.175476,    36.175684,    36.176639,    36.176357,    36.176904,
        36.176824,    36.177783,    36.176241,    36.175586,    36.175534,    36.175001,    36.175169,    36.175824,
        36.175251,    36.174614,    36.176239,    36.174978,    36.174552,    36.173868,    36.173979,    36.173324,
        36.173668,    36.172804,    36.173362,    36.173154,    36.172636,    36.172345,    36.179078,    36.175789,
        36.171613,    36.174551,    36.172856,
    ]
    ,
                  lon=[
        -85.50859,    -85.507171,    -85.507844,    -85.507895,    -85.507414,    -85.506856,    -85.507274,    -85.506803,
        -85.506355,    -85.506229,    -85.506500,    -85.507472,    -85.506594,    -85.506946,    -85.505949,    -85.505650,
        -85.506058,    -85.506704,    -85.506659,    -85.505845,    -85.507426,    -85.503264,    -85.502857,    -85.504391,
        -85.505096,    -85.504741,    -85.503356,    -85.503155,    -85.50275,    -85.5025,    -85.50336,    -85.504218,
        -85.504641,    -85.504116,    -85.505069,    -85.504076,    -85.504802,    -85.503713,    -85.504642,    -85.503708,
        -85.504481,    -85.504775,    -85.504662,    -85.505466,    -85.503819,    -85.504863,    -85.509369,    -85.50022,
        -85.504513,    -85.508593,    -85.510705,
    ]

    # To access individual elements, you can use indexing, e.g., data[0] will give you -85.50859.
    ,
                  name=[ "Ray Morris Hall",    "Emergency Posts Cooper & Dunn Halls",    "Browning Hall",    "Evins Hall",
        "Cooper Hall",    "Dunn Halls",    "Ellington Hall",    "Warf Hall",
        "Maddux Hall",    "McCord",    "Emergency Posts Maddux & McCord Halls",    "Laboratory Science Commons",
        "Foundry",    "Stonecipher Lecture Hall",    "Lewis Hall",    "Emergency Post Lewis Hall",
        "Angelo & Jennette Volpe Library",    "Brown Hall",    "Bruner Hall",    "Clement Hall",
        "Prescott Hall",    "Jobe Hall",    "Murphy Hall",    "Pennebaker Hall",
        "Johnson Hall",    "Bryan Fine Arts Building",    "M.S. Cooper",    "Pinkerton Hall",
        "New Hall North",    "New Hall South",    "Emergency Post New Hall North",    "Roaden University Center",
        "Henderson Hall",    "Derryberry Hall",    "Foster Hall",    "Emergency Post Derryberry Hall",
        "TJ Farr Building",    "Kittrell Hall",    "Bartoo Hall",    "Jere Whitson Building",
        "Emergency Post Bartoo Hall",    "Matthews-Daniel Hall",    "Memorial Gym",    "Military Science Building",
        "Oakley Hall",    "Crawford Hall",    "Academic Wellness Center",    "Foundation Hall",
        "Robert and Gloria Bell Hall",    "Southwest Hall",    "Marc L. Burnett Student Recreation and Fitness Center"
    ],
                  glyph=["https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41416/WDM_Campus-Map_Icon-Template_Emergency.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41416/WDM_Campus-Map_Icon-Template_Emergency.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41416/WDM_Campus-Map_Icon-Template_Emergency.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40632/WDM_Campus-Map_Residential-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41416/WDM_Campus-Map_Icon-Template_Emergency.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41417/WDM_Campus-Map_Icon-Template_Admin.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41417/WDM_Campus-Map_Icon-Template_Admin.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41416/WDM_Campus-Map_Icon-Template_Emergency.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41417/WDM_Campus-Map_Icon-Template_Admin.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41416/WDM_Campus-Map_Icon-Template_Emergency.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41417/WDM_Campus-Map_Icon-Template_Admin.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40631/WDM_Campus-Map_Academic-Buildings_30px.png",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/41417/WDM_Campus-Map_Icon-Template_Admin.png",
    ],
                  color = ["#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF0000", "#FF0000",
                          "#008080", "#008080", "#008080", "#008080", "#008080",
                          "#800080", "#800080", "#800080", "#800080", "#800080",
                          "#808080", "#808080", "#808080", "#808080", "#808080",
                          "#FFA500", "#FFA500", "#FFA500", "#FFA500", "#FFA500",
                          "#A52A2A", "#A52A2A", "#A52A2A", "#A52A2A", "#A52A2A",
                          "#FFC0CB", "#FFC0CB", "#FFC0CB", "#FFC0CB", "#FFC0CB",
                          "#008000", "#008000", "#008000", "#008000", "#008000",
                          "#FFFF00", "#FFFF00", "#FFFF00", "#FFFF00", "#FFFF00",
                          "#0000FF", "#0000FF", "#0000FF", "#0000FF", "#0000FF"],
                  font = ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF",
                          "#000000", "#000000", "#000000", "#000000", "#000000",
                          "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF",
                          "#000000", "#000000", "#000000", "#000000", "#000000",
                          "#000000", "#000000", "#000000", "#000000", "#000000",
                          "#000000", "#000000", "#000000", "#000000", "#000000",
                          "#000000", "#000000", "#000000", "#000000", "#000000",
                          "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF",
                          "#000000", "#000000", "#000000", "#000000", "#000000",
                          "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"]
    ,
                  imgs = ["https://cdn.maps.moderncampus.net/uploads/icon/image/39283/RMH_Stock_OCM_Map_Project_Ray_Morris_Hall_15_October_2021_00002.jpg",
                          "https://cdn.maps.moderncampus.net/uploads/icon/image/39223/COOP-DUNN_Stock_Cooper_Dunn_12MAY21_00003.jpg" ,
                          "https://cdn.maps.moderncampus.net/uploads/icon/image/39216/BRNG-EVIN_Stock_Res_Life_Browning_Evins_Exterior_1JUN21_00001.jpg",
                          "https://cdn.maps.moderncampus.net/uploads/icon/image/39216/BRNG-EVIN_Stock_Res_Life_Browning_Evins_Exterior_1JUN21_00001.jpg",
                          "https://cdn.maps.moderncampus.net/uploads/icon/image/39223/COOP-DUNN_Stock_Cooper_Dunn_12MAY21_00003.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39223/COOP-DUNN_Stock_Cooper_Dunn_12MAY21_00003.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39225/ELLG_Stock_Res_Life_Ellington_Warf_Exterior_1JUN21_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39225/ELLG_Stock_Res_Life_Ellington_Warf_Exterior_1JUN21_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39259/MDDX_Stock_Res_Life_Maddux_McCord_Exterior_1JUN21_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39259/MDDX_Stock_Res_Life_Maddux_McCord_Exterior_1JUN21_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39259/MDDX_Stock_Res_Life_Maddux_McCord_Exterior_1JUN21_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40640/LSC_Scenes_Campus_Spring_Flowers_23MAR21_00018.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39234/FDRY_Stock_OCM_Map_Project_Foundry_27SEP21_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39289/SLH_Stock_OCM_Map_Project_Stonecipher_Lecture_Hall_27SEP21_00004.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39257/LEWS_Stock_OCM_Map_Project_Lewis_Hall_27SEP21_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39257/LEWS_Stock_OCM_Map_Project_Lewis_Hall_27SEP21_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39308/LIBR_Stock_Campus_Drone_23AUG19_00039.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39214/BRWN_Stock_OCM_Map_Project_Brown_Hall_15_October_2021_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39218/BRUN_Stock_OCM_Map_Project_Bruner_Hall_27SEP21_0000-1.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39222/CLEM_Stock_OCM_Map_Project_Clement_Hall_27SEP21_0000-1.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39282/PRSC_Stock_OCM_Map_Project_Prescott_Hall_15_October_2021_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39241/JOBE_Stock_Jobe_exterior_5NOV20_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39241/JOBE_Stock_Jobe_exterior_5NOV20_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39278/PENN_Stock_Pennebaker_exterior_5NOV20_00003.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39208/JOHN-Stock_OCM_Map_Project_Johnson_Hall_27SEP21_00007-1.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39221/BFA_Stock_Bryan_Fine_Arts_exterior_5NOV20_00001.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39258/MSCP_Stock_Aerial_Campus_22APR21_00111.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39258/MSCP_Stock_Aerial_Campus_22APR21_00111.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39272/NEWN_Stock_Res_Life_New_Hall_North_Exterior_1JUN21_00004.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39275/NEWS_Scenes_Aerial_Campus_NHS_5OCT21_00013.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39272/NEWN_Stock_Res_Life_New_Hall_North_Exterior_1JUN21_00004.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39199/Stock_OCM_Map_Project_Roaden_University_Center_27SEP21_00001.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40854/HEND_Stock_CampusBuildings_HEND_10JUN22_00002.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40767/DBRY_Scenes_Aerial_Derryberry_Hall_Quad_29APR22_00065.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39231/FOST_Scenes_Aerial_Campus_Foster_Hall_5OCT21_00017.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40767/DBRY_Scenes_Aerial_Derryberry_Hall_Quad_29APR22_00065.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40853/FARR_Stock_CampusBuildings_FARR_10JUN22_00007.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40848/KITT_Stock_CampusBuildings_KITT_10JUN22_00005.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40845/BART_Stock_CampusBuildings_BART_10JUN22_00005.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40836/JWB_Stock_Campus_Drone_23AUG19_00055.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40845/BART_Stock_CampusBuildings_BART_10JUN22_00005.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40642/MATT-DANL_Scenes_Fall_Color_Stock_5NOV20_00030.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39269/MGYM_Stock_MGYM_Memorial_Gym_exterior_5NOV20_00003.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39271/ROTC_Stock_OCM_Map_Project_Military_Science_27SEP21_00001.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39277/OKLY_Stock_OCM_Map_Project_Oakley_Hall_27SEP21_00001.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39227/CRAW_Stock_Res_Life_Crawford_Exterior_1JUN21_00005.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39210/AWC_Stock_Academic_Wellness_Ctr__12JUL21_00001.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39232/Stock_Campus_Drone_23AUG19_00100.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/40849/BELL_Stock_CampusBuildings_BELL_10JUN22_00001.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39288/SWH_Stock_OCM_Map_Project_Southwest_Hall_15_October_2021_0000-1.jpg",
    "https://cdn.maps.moderncampus.net/uploads/icon/image/39266/MBRC_Stock_Aerial_Campus_22APR21_00075.jpg",
    ],
                  meter_id= geo_data['meter_id'],
                  rate = geo_data['participation'],
                  delta= geo_data['delta_value'],
    ))
    md.sort_values(by = "delta",inplace = True,ascending = False)
    map_source = ColumnDataSource(
        data=dict(lat= md["lat"],
                  lon=md["lon"],
                  name=md["name"],
                  glyph=md["glyph"],
                  color = md['color'],
                  font = md['font'],
                  imgs = md['imgs'],
                  meter_id= md['meter_id'],
                  rate = md['rate'],
                  delta= md['delta'],
    ))

    circle= p.circle(x="lon", y="lat", size=30, fill_alpha=0,line_alpha=0, source=map_source)
    color_circle = p.circle(x="lon", y="lat", size=0, fill_color = "color",line_color = "color", source=map_source)
    image_render = p.image_url(url="glyph", x = "lon", y="lat",anchor='bottom_center',source= map_source)


    hvr = HoverTool(renderers = [circle],tooltips=TOOLTIPS)
    p.add_tools(hvr)

    gd = pd.DataFrame(dict(org_name = ["ABC Corporation", "Acme Widget Manufacturing",
                                  "Global Logistics Inc.", "Infinite Innovations",
                                  "MegaMart Superstores", "Pacific Shipping Services",
                                  "Software Solutions Co.", "Tech Innovators Ltd.",
                                  "United Builders Group", "XYZ Industries"],
                      delta = [ 17726.14,15095.46,
                                14483.65,8073.15,
                                14836.41,8765.90,
                                8966.68,8154.62,
                                11472.43,12655.76,],
                      groupy = [36.1727,36.173052,
                                36.174239,36.176,
                                36.1775,36.1755,
                                36.175824,36.174,
                                36.172804,0],
                      groupx = [-85.508,-85.5065,-85.5066,-85.5066,-85.5041,-85.503277,-85.5046,-85.504,-85.504775,0],
                      color = ["#FF0000","#008080","#800080","#808080","#FFA500","#A52A2A","#FFC0CB","#008000","#FFFF00","0"]))
    gd.sort_values(by = "delta",inplace = True,ascending = False,ignore_index = True)
    gsource = ColumnDataSource(
        data=dict(groupy = gd["groupy"],
    groupx = gd["groupx"],
    color = gd["color"],
    g = gd["org_name"],
    ))


    zsource = ColumnDataSource(
        data=dict(groupy = [36.179078, 36.175789, 36.171613, 36.174551, 36.172856],
    groupx = [-85.509369, -85.50022, -85.504513, -85.508593, -85.510705],
    color = ["#0000FF","#0000FF","#0000FF","#0000FF","#0000FF"],
    ))

    area_data = pd.DataFrame(gsource.data)
    for i,r in area_data.iterrows():
      if r["g"] == "XYZ Industries":
        p.circle(x="groupx",y="groupy",fill_color = "color", line_color = "color", size=50,fill_alpha=0.3,legend_label="{i}: {r}".format(i = str(i+1),r =r["g"]), source = zsource)
      else: p.circle(x=r["groupx"],y=r["groupy"],fill_color = r["color"], line_color = r["color"], size=140,fill_alpha=0.3,legend_label="{i}: {r}".format(i = str(i+1),r =r["g"]))
    p.legend.title = "Organization Ranking"

    #--------------------------------------------------
    geo_tab = TabPanel(child = p,title = "Ranking")
    pacf_tab = TabPanel(child = row(pacf), title = "PACF")
    acf_tab = TabPanel(child = row(acf), title = "ACF")

    tabs = Tabs(tabs=[geo_tab,acf_tab,pacf_tab])
    tabs.visible = False
  #----------------------------------------------------
    button = Button(label="More Details", button_type="success")

    button.js_on_event("button_click", CustomJS(args=dict(tabs = tabs),code="""
    tabs.visible = !(tabs.visible)"""))
    return column(column(row(column(row(legend_figure,row(total_card),pie,column(row(org_select,meter_select),row(event_select,Spacer(width=30),column(Spacer(height = 20),button)))), row(fig))),tabs))

def data_source_org(session_id,meter_id):
   return None

def data_source_user(session_id,meter_id):
   return None

def test_bokeh_json_dumps(session_id):
  session_data, _ = get_session_data(session_id)
  meter_ids, _ = linked_meter_ids(session_data['account_id'])
  meter_id = meter_ids[0]
  org_id, _ = get_user_org(session_data['account_id'])

  return json.dumps(json_item(data_source_admin(session_id,meter_id,org_id)))
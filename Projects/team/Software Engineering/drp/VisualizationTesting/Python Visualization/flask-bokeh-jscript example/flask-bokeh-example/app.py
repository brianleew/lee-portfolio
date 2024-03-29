import json

from flask import Flask, request,render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.resources import CDN
from bokeh.embed import json_item

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool, HoverTool

from sqlalchemy import create_engine,text
import pandas as pd
import numpy as np

#user = 'root'
#password = 'NewPassword'
#host = '127.0.0.1'
#port = 3306
#database = 'demand_response_portal'

#engine = create_engine(url="mysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
#conn = engine.connect()


#query = text("select meter_data.value as power, meter_data.start_time as start from meter_data where meter_data.meter_name = 'Total'")
#GetSQLTest = pd.read_sql_query(query,conn)
#GetSQLTest['start'] =  pd.to_datetime(GetSQLTest['start'], format='%Y-%m-%d %H:%M:%S')
#GetSQLTest["sd"] = GetSQLTest['start'].dt.date.copy()
#GetSQLTest['sm'] = [s.replace(day=1) for s in GetSQLTest['start'].dt.date].copy()
#Annual = GetSQLTest[["sm","power"]].groupby('sm',as_index = False).sum()
#m = GetSQLTest["sm"].unique()[0]
#Month = GetSQLTest[["sm","sd","power"]].groupby(["sm","sd"],as_index = False).sum().query("sm == @m")[["sd","power"]]
#d = GetSQLTest["sd"].unique()[0]
#Daily = GetSQLTest[['start',"sd","power"]].query("sd == @d")[["start", "power"]]
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("Login.html")

@app.route('/register')
def register():
    return render_template("RegisterAcct.html")

@app.route('/bokeh')
def bokeh():

    fig = figure(title = "Total Annual Line Graph",x_axis_type = "datetime")
    fig1 = fig.line(source = Annual,x="sm",y="power",line_width = 2,color='red')
    fig.square(source = Annual,x="sm",y="power",size = 20,color='red')
    fig.add_tools(HoverTool(renderers=[fig1], tooltips=[('power',"@power")],mode='vline'))

    #pig = figure(title = "Total Month Line Graph",x_axis_type = "datetime")
    #pig1 = pig.line(source = Month,x="sd",y="power",line_width = 2,color='navy')
    #pig.circle(source = Month,x="sd",y="power",size = 20,color='navy')
    #pig.add_tools(HoverTool(renderers=[pig1], tooltips=[('power',"@power")],mode='vline'))

    dig = figure(title = "Total Day Line Graph",x_axis_type = "datetime")
    dig1 = dig.line(source = Daily,x="start",y="power",line_width = 2,color='green')
    dig.triangle(source = Daily,x="start",y="power",size = 20,color='green')
    dig.add_tools(HoverTool(renderers=[dig1], tooltips=[('power',"@power")],mode='vline'))
    
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    script1, div1 = components(pig)
    script2, div2 = components(dig)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        plot_script1=script1,
        plot_div1=div1,
        plot_script2=script2,
        plot_div2=div2,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return html

@app.route('/dashboard')
def dashboard():
        # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    
    
    #fig = figure(title = "Total Annual Line Graph",x_axis_type = "datetime")
    #fig1 = fig.line(source = Annual,x="sm",y="power",line_width = 2,color='red')
    #fig.square(source = Annual,x="sm",y="power",size = 20,color='red')
    #fig.add_tools(HoverTool(renderers=[fig1], tooltips=[('power',"@power")],mode='vline'))

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    #script, div = components(fig)
    #html = render_template(
    #    'dashboard.html',
    #    plot_script=script,
    #    plot_div=div,
    #    js_resources=js_resources,
    #    css_resources=css_resources,
    #)
    #return html
    return render_template('dashboard.html',js_resources=js_resources, css_resources=css_resources)

@app.route('/table')
def html_table():

    return render_template('table.html',  tables=[GetSQLTest.to_html(classes='data')], titles=GetSQLTest.columns.values)

@app.route('/plot/<int:Number>/<string:Q>') # need to rember the converters <int:?> and <string:?> for getting the information you need
def plot(Number,Q): #this works that means you can pass in the member id and password
                  # to flask and use in retreiving the information from the database
    #print([Number,Q])
    if Number == 1:
        user = 'root'
        password = 'NewPassword'
        host = '127.0.0.1'
        port = 3306
        database = 'demand_response_portal'

        engine = create_engine(url="mysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
        conn = engine.connect()

        squery = "select meter_data.value as power, meter_data.start_time as start from meter_data where meter_data.meter_name = '{}';".format(Q)
        query = text(squery)
        GetSQLTest = pd.read_sql_query(query,conn)
        GetSQLTest['start'] =  pd.to_datetime(GetSQLTest['start'], format='%Y-%m-%d %H:%M:%S')
        GetSQLTest["sd"] = GetSQLTest['start'].dt.date.copy()
        GetSQLTest['sm'] = [s.replace(day=1) for s in GetSQLTest['start'].dt.date].copy()
        Annual = GetSQLTest[["sm","power"]].groupby('sm',as_index = False).sum()
        m = GetSQLTest["sm"].unique()[0]
        Month = GetSQLTest[["sm","sd","power"]].groupby(["sm","sd"],as_index = False).sum().query("sm == @m")[["sd","power"]]
        d = GetSQLTest["sd"].unique()[0]
        Daily = GetSQLTest[['start',"sd","power"]].query("sd == @d")[["start", "power"]]
        
        Title = "{} Month Line Graph".format(Q)
        pig = figure(title = Title,x_axis_type = "datetime",sizing_mode="scale_both")
        pig1 = pig.line(source = Month,x="sd",y="power",line_width = 2,color='navy')
        pig.circle(source = Month,x="sd",y="power",size = 20,color='navy')
        pig.add_tools(HoverTool(renderers=[pig1], tooltips=[('power',"@power")],mode='vline'))
    #p = make_plot('petal_width', 'petal_length')
        return json.dumps(json_item(pig))
    
    if Number == 2:
        user = 'root'
        password = 'NewPassword'
        host = '127.0.0.1'
        port = 3306
        database = 'demand_response_portal'

        engine = create_engine(url="mysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
        conn = engine.connect()

        squery = "select meter_data.value as power, meter_data.start_time as start from meter_data where meter_data.meter_name = '{}';".format(Q)
        query = text(squery)
        GetSQLTest = pd.read_sql_query(query,conn)
        GetSQLTest['start'] =  pd.to_datetime(GetSQLTest['start'], format='%Y-%m-%d %H:%M:%S')
        GetSQLTest["sd"] = GetSQLTest['start'].dt.date.copy()
        GetSQLTest['sm'] = [s.replace(day=1) for s in GetSQLTest['start'].dt.date].copy()
        Annual = GetSQLTest[["sm","power"]].groupby('sm',as_index = False).sum()
        m = GetSQLTest["sm"].unique()[0]
        Month = GetSQLTest[["sm","sd","power"]].groupby(["sm","sd"],as_index = False).sum().query("sm == @m")[["sd","power"]]
        d = GetSQLTest["sd"].unique()[0]
        Daily = GetSQLTest[['start',"sd","power"]].query("sd == @d")[["start", "power"]]
        
        tle = "{} Day Line Graph".format(Q)
        dig = figure(title = tle, x_axis_type = "datetime",sizing_mode="scale_both")
        dig1 = dig.line(source = Daily,x="start",y="power",line_width = 2,color='green')
        dig.triangle(source = Daily,x="start",y="power",size = 20,color='green')
        dig.add_tools(HoverTool(renderers=[dig1], tooltips=[('power',"@power")],mode='vline'))
        return json.dumps(json_item(dig))
    
@app.route("/layout")
def layout():
    Q = request.args.get('meter_name')
    user = 'root'
    password = 'NewPassword'
    host = '127.0.0.1'
    port = 3306
    database = 'demand_response_portal'

    engine = create_engine(url="mysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
    conn = engine.connect()

    squery = "select meter_data.value as power, meter_data.start_time as start from meter_data where meter_data.meter_name = '{}';".format(Q)
    query = text(squery)
    GetSQLTest = pd.read_sql_query(query,conn)

    squery = "select * from meter_prediction where meter_prediction.meter_name = '{}';".format(Q)
    query = text(squery)
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

@app.route('/handle_data', methods=['POST'])
def handle_data():
    return request.form['projectFilepath']

@app.route('/plot2')
def plot2():
    user = 'root'
    password = 'NewPassword'
    host = '127.0.0.1'
    port = 3306
    database = 'demand_response_portal'

    engine = create_engine(url="mysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
    conn = engine.connect()


    query = text("select meter_data.value as power, meter_data.start_time as start from meter_data where meter_data.meter_name = 'Total';")
    GetSQLTest = pd.read_sql_query(query,conn)
    GetSQLTest['start'] =  pd.to_datetime(GetSQLTest['start'], format='%Y-%m-%d %H:%M:%S')
    GetSQLTest["sd"] = GetSQLTest['start'].dt.date.copy()
    GetSQLTest['sm'] = [s.replace(day=1) for s in GetSQLTest['start'].dt.date].copy()
    Annual = GetSQLTest[["sm","power"]].groupby('sm',as_index = False).sum()
    m = GetSQLTest["sm"].unique()[0]
    Month = GetSQLTest[["sm","sd","power"]].groupby(["sm","sd"],as_index = False).sum().query("sm == @m")[["sd","power"]]
    d = GetSQLTest["sd"].unique()[0]
    Daily = GetSQLTest[['start',"sd","power"]].query("sd == @d")[["start", "power"]]

    fig = figure(title = "Total Annual Line Graph",x_axis_type = "datetime",sizing_mode="scale_both")
    fig1 = fig.line(source = Annual,x="sm",y="power",line_width = 2,color='red')
    fig.square(source = Annual,x="sm",y="power",size = 20,color='red')
    fig.add_tools(HoverTool(renderers=[fig1], tooltips=[('power',"@power")],mode='vline'))
    #p = make_plot('sepal_width', 'sepal_length')
    return json.dumps(json_item(fig))


if __name__ == '__main__':
    app.run(debug=False)
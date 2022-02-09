from motion_detector import df
from bokeh.plotting import figure,show,output_file
from bokeh.models import DatetimeTickFormatter, HoverTool,ColumnDataSource
from datetime import datetime,timedelta

df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df)

p=figure(x_axis_type="datetime",sizing_mode="stretch_width",plot_height=250,title="Motion Graph")
p.yaxis.ticker.desired_num_ticks=1
p.yaxis.minor_tick_line_color=None

hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])
p.add_tools(hover)

p.quad(left="Start",right="End",top=1,bottom=0,fill_color="green",source=cds)
# p.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

output_file("Graph.html")
show(p)

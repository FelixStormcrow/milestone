import bokeh.plotting as plt
import os, re

def compute(dic,ticker):
	t=dic['time']
	p = plt.figure(title='Stock data for'+ticker,x_axis_label='time',y_axis_label='price',x_axis_type="datetime")
	data_n=['open','close','adj_open','adj_close']
	col=['black','blue','red','green']
	i=0
	for key in data_n:
		if key in dic.keys():
			p.line(t,dic[key],legend=key,line_color=col[i], line_width=2)
			i+=1
	p.legend.location='top_left'
	from bokeh.resources import CDN
	from bokeh.embed import components
	script, div = components(p)
	head = """
<link rel="stylesheet"
 href="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.css"
 type="text/css" />
<script
 src="http://cdn.pydata.org/bokeh/release/bokeh-0.9.0.min.js">
</script>
"""
	return head, script, div

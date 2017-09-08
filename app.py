from flask import Flask, render_template, request, redirect
import pandas as pd
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool
from bokeh.embed import components
import quandl
quandl.ApiConfig.api_key = "zhKcDxjgVzwBFH6tyFyh"

app = Flask(__name__)

# Load the Iris Data Set
# iris_df = pd.read_csv("data/iris.data", 
#     names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
# feature_names = iris_df.columns[0:-1].values.tolist()

def get_data(ticker):
	#https://www.quandl.com/api/v3/datasets/EOD/AAPL.json?rows=31&order=desc&column_index=4&api_key=YOURAPIKEY
	if ticker == "":
		return ""
	try:
		data = quandl.get("EOD/" + ticker, rows = 30, column_index = 4, returns = "pandas")
	except quandl.errors.quandl_error.ForbiddenError:
		return ""
	return data

def make_plot(ticker, data):
	p1 = figure(x_axis_type="datetime", title="Stock Closing Prices " + ticker)
	p1.grid.grid_line_alpha=0.3
	p1.xaxis.axis_label = 'Date'
	p1.yaxis.axis_label = 'Price'
	if ticker == "" or data == "":
		return p1
	p1.line(data.index, data['Close'], color='#A6CEE3', legend=ticker)
	p1.legend.location = "top_left"
	return p1

# Create the main plot
# def create_figure(current_feature_name, bins):
# 	p = Histogram(iris_df, current_feature_name, title=current_feature_name, color='Species', 
# 	 	bins=bins, legend='top_right', width=600, height=400)
# 
# 	# Set the x axis label
# 	p.xaxis.axis_label = current_feature_name
# 
# 	# Set the y axis label
# 	p.yaxis.axis_label = 'Count'
# 	return p

# Index page
@app.route('/')
def index():
	my_ticker = request.args.get("ticker")
	if my_ticker == None:
		my_ticker = ""
	data = get_data(my_ticker)
	plot = make_plot(my_ticker, data)
	script, div = components(plot)
	return render_template("ticker_index.html", ticker = my_ticker, script = script, div = div)
# 	# Embed plot into HTML via Flask Render
 	
	#return render_template("ticker_index.html", ticker = my_ticker) #, script=script, div=div,
#		feature_names=feature_names,  current_feature_name=current_feature_name)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)
	

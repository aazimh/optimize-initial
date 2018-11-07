from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import optimize
import draw
import json

app = Flask(__name__)

#dates array for use later
dates = ['1/1/2017','1/8/2017','1/15/2017','1/22/2017','1/29/2017','2/5/2017','2/12/2017','2/19/2017','2/26/2017','3/5/2017','3/12/2017','3/19/2017','3/26/2017','4/2/2017','4/9/2017','4/16/2017','4/23/2017','4/30/2017','5/7/2017','5/14/2017',
	'5/21/2017','5/28/2017','6/4/2017','6/11/2017','6/18/2017','6/25/2017','7/2/2017','7/9/2017','7/16/2017','7/23/2017','7/30/2017','8/6/2017','8/13/2017','8/20/2017','8/27/2017','9/3/2017','9/10/2017','9/17/2017','9/24/2017','10/1/2017',
	'10/8/2017','10/15/2017','10/22/2017','10/29/2017','11/5/2017','11/12/2017','11/19/2017','11/26/2017','12/3/2017','12/10/2017','12/17/2017','12/24/2017','12/31/2017']

BASE_NUM = 134

#random function needed for passing to html
def html_input(c):
    return '<input name="{}" value="{{}}" style="margin:0 auto"/>'.format(c)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/contact")
def contact():
    return "Contact us!"

@app.route("/about")
def about():
    return "About us!"	

# print out input form
@app.route("/forecast")
def forecast():
	step1 = pd.read_excel('template.xlsx',index_col=0)
	step1.index = step1.index.strftime("%d %b %Y")
	print(step1.index)
	return render_template('forecast.html',testval=step1.style.format({c: html_input(c) for c in step1.columns}).render())
	
# method to take submitted form and ideally parse as df and print
@app.route("/calc_forecast", methods=['POST'])
def calc_forecast():
	
	#take submitted laydown and remove the random last row
	return_dict = request.values.to_dict(flat=False)
	return_dict.pop('last', None)
	
	#load into dataframe
	df = pd.DataFrame(return_dict)
	
	#change index to dates
	df.index = dates
	
	#replace blanks with zeroes
	df = df.replace(r'^\s*$', 0, regex=True)
	
	print('----applying ad stock------')
	output, mediaspend = optimize.applyAdStock(df)
	print('----applying dim returns------')
	output = optimize.applyDimReturns(output)
	print('----applying coefficients------')
	output = optimize.applyCoeff(output)
	output = output.round(decimals=2)

	print('this is the result of the calcs')
	# print(output)
	
	totalsales = "{:,}".format(int(output.values.sum() + BASE_NUM*len(dates)))
	mediasales = "{:,}".format(int(output.values.sum()))
	mediacontrib = "{:.1%}".format(output.values.sum()/float(output.values.sum() + BASE_NUM*len(dates)))
	
	

	print('The total sales are ', totalsales)
	print('The total media sales are ', mediasales)
	print('The media contribution is ', mediacontrib)
	print('The media spend is ', mediaspend)
	
	summary = {}
	summary['totalsales'] = totalsales
	summary['mediasales'] = mediasales
	summary['mediacontrib'] = mediacontrib
	summary['mediaspend'] = mediaspend
	
	returnarr = [draw.reorganize(output.to_json(orient='split'), BASE_NUM)]
	returnarr.append(summary)
	
	# print(output.to_json(orient='split'))
	
	return json.dumps(returnarr)
from ast import literal_eval
import datetime as dt
from dateutil.parser import parse

def reorganize(data, base_num):
	data = literal_eval(data)
	cols = data['columns']
	dates2 = data['index']
	dates3 = [w.replace('\\', '') for w in dates2]
	dates4 = [parse(date).strftime('"%d %b %Y"') for date in dates3]
	dates = [w.replace('"', '') for w in dates4]
	data = data['data']
	returndata = []
	
	dataPoints = []

	#add base to chart data
	base = {}
	base['type'] = "stackedColumn"
	base['name'] = "Base"
	base['showInLegend'] = True
	for i in range(0,len(dates)):
		dataPoints.append({'y' : base_num, 'label': dates[i]})
	base['dataPoints'] = dataPoints
	returndata.append(base)
	
	i=0
	#add all other channels to chart data
	for channel in cols:
		temp = {}
		temp['type'] = "stackedColumn"
		temp['name'] = channel
		temp['showInLegend'] = True
		dataPoints = []
		j=0
		for point in data:
			# print('the point in data is ',point)
			dataPoints.append({'y': point[i], 'label': dates[j]})
			j+=1
		temp['dataPoints'] = dataPoints
		returndata.append(temp)
		i+=1

	options = {
		'data': returndata
	}
	
	# print('the options being sent are')
	# print(options)
	
	return options		
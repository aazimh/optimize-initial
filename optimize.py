import pandas as pd
import math
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:,.02f}'.format

ADSTOCKS = {
	'Radio': 0.1,
	'TV': 0.7,
	'Digital': 0.9
}

DR = {
	'Radio' : [5000, 5],
	'TV' : [320, 1],
	'Digital' : [525000, 3]
}

COEFF = {
	'Radio' : 32.4,
	'TV': 66.48,
	'Digital' : 8.32
}

DIVISORS = {
	'Radio': 1,
	'TV' : 143,
	'Digital' : 0.006
}
	
def applyAdStock(df):
	step2 = df
	mediaspend=0
	for column in df:
		df[column] = df[column].apply(pd.to_numeric)
		mediaspend += df[column].values.sum()
		# print(df.dtypes)
		# print(column)
		# print('Ad stock is %d' % (ADSTOCKS[column]*100))
		adstock = ADSTOCKS[column]
		divisor = DIVISORS[column]
		df[column] = df[column]/divisor
		for i in range(0,len(df[column])):
			if i==0:
				step2.iloc[i, step2.columns.get_loc(column)] = df.iloc[i].loc[column]
			else:
				step2.iloc[i, step2.columns.get_loc(column)] = df.iloc[i].loc[column] + (step2.iloc[i-1].loc[column] * adstock)
	return step2, "$" + "{:,}".format(mediaspend)
				# print('value is ',step2.iloc[i].loc[column])
				# print('valuedf is ',df.iloc[i].loc[column])
				# print('valuedfprev is ',df.iloc[i-1].loc[column])
				# print('value adstock is ',adstock)

def applyDimReturns(df):
	step3 = df
	for column in df:
		# print(column)
		# print('Ad stock is %d' % (ADSTOCKS[column]*100))
		dr1 = DR[column][0]
		dr2 = DR[column][1]
		for i in range(0,len(df[column])):
			step3.iloc[i, step3.columns.get_loc(column)] = math.atan((((df.iloc[i].loc[column]**2)*dr2)/(dr1**2))/(math.pi/2))
	return step3
			# print('value is ',step2.iloc[i].loc[column])
			# print('valuedf is ',df.iloc[i].loc[column])
			# print('valuedfprev is ',df.iloc[i-1].loc[column])

def applyCoeff(df):
	step4 = df
	for column in df:
		# print(column)
		# print('Ad stock is %d' % (ADSTOCKS[column]*100))
		coeff = COEFF[column]
		for i in range(0,len(df[column])):
			step4.iloc[i, step4.columns.get_loc(column)] = df.iloc[i].loc[column] * coeff
	return step4
			# print('value is ',step2.iloc[i].loc[column])
			# print('valuedf is ',df.iloc[i].loc[column])
			# print('valuedfprev is ',df.iloc[i-1].loc[column])



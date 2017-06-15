from flask import Flask, render_template, request, redirect
import pandas as pd
import datetime as dt  
from fig_gen import compute
import dateutil.parser as parser

app_dimp = Flask(__name__)

data_n=['open','close','adj_open','adj_close']
app_dimp.inputvars={}

for key in data_n:
	app_dimp.inputvars[key]='0'
app_dimp.inputvars['time_interval']='0'
app_dimp.inputvars['startdate']='0'
app_dimp.inputvars['enddate']='0'
app_dimp.inputvars['ticker']='AAPL'


def assemble_string():
	str_base='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='  
	str_col='&qopts.columns=date'
	for key in data_n:
		if app_dimp.inputvars[key] == '1': str_col=str_col+','+key
	str_api='&api_key=cfG6Lxrn_4Pg8J8jLodw'
	ticker=app_dimp.inputvars['ticker']
        str_time=assemble_time(app_dimp.inputvars['time_interval'],app_dimp.inputvars['startdate'],app_dimp.inputvars['enddate'])
        return str_base+ticker+str_col+str_time+str_api

def assemble_time(cat, start, end):
	if cat != '-1':
		end_date=dt.date.today()
		start_date=end_date-pd.tseries.offsets.DateOffset(months=int(cat))
        else:
                end_date=parser.parse(end)
                start_date=parser.parse(start)
        return '&date.gte='+start_date.strftime('%Y%m%d')+'&date.lte='+end_date.strftime('%Y%m%d')
		


@app_dimp.route('/')
def main():
	return redirect('/index')

@app_dimp.route('/index',methods=['GET'])
def init_get_info():
	return render_template('index.html')

@app_dimp.route('/figure',methods=['POST'])
def proc_get_info():
	for key in app_dimp.inputvars:
		if key in request.form:
			app_dimp.inputvars[key]=request.form[key]
		else:
			app_dimp.inputvars[key]='0'
	
	if sum([int(app_dimp.inputvars[key]) for key in data_n])==0:
		return render_template('error.html',err='No data requested!')	


	assembled_string=assemble_string()
        f = open('quandl_string.txt','w')
	f.write(assembled_string)
	f.close()
	df = pd.read_json(assembled_string)
	data= df['datatable']['data']
	
	if len(data)==0:
		#no data, probably bad ticker
		return render_template('error.html',err='Data empty, might be a bad ticker!')

	columns={}
	for i, column in enumerate(df['datatable']['columns']):
		columns[column['name']]=i
	

	data_dic={}	
	dd = [dat[columns['date']] for dat in data]
	data_dic['time'] = [d.date() for d in pd.to_datetime(dd)]
	
	for key in data_n:
		if app_dimp.inputvars[key]=='1': data_dic[key]=[dat[columns[key]] for dat in data]

	result=compute(data_dic,app_dimp.inputvars['ticker'])

  	return render_template('figure.html', result=result)



if __name__ == '__main__':
    app_dimp.run(host='0.0.0.0',debug=True)

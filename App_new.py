# This Python file uses the following encoding: utf-8
# encoding: utf-8
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from functools import wraps
import requests
import json
import datetime
import pandas as pd
import os
import shutil
import datetime

app = Flask(__name__, static_folder='static', static_url_path='')


@app.route('/', methods=['GET', 'POST'])
def index():

	if request.method == 'POST':
		Data = pd.read_csv("Data.csv")
		Old_Data = Data.to_dict('records')
		Data_row = []
		d = {}
		d['Yourname'] = request.form.get('yourname',"")
		d['Yourdepartment'] = request.values.get('yourdepartment',"")
		d['Context'] = request.values.get('txtMsg',"")
		d['Receiver'] = request.values.get('receiver',"")
		d['Receiverdepartment'] = request.values.get('receiverdepartment',"")

		textnum = len(d['Context'])

		#list() 強迫轉型，才能使用count函數
		check_is_legal = list(d.values()).count("")

		# 如果沒有拿到空字串的話 (使用者全部的東西都有輸入)
		if (check_is_legal == 0 and textnum <= 100):

			Data_row.append(d)
			NewData = Data_row + Old_Data
			df = pd.DataFrame(NewData)
			df.to_csv('Data.csv',encoding='utf_8_sig', index=False)
			return redirect(url_for('Success'))

		elif textnum > 100:
			textoutlimit = textnum
			return render_template("index.html",textoutlimit = textnum)

		# 若字數小於100 但沒有全部填的情形
		else:
			error = 'Please fill the whole form'
			return render_template("index.html",error = error)

	return render_template("index.html")


@app.route("/Success")
def Success():
	return render_template("sucess.html")

@app.route("/TextBoard")
def TextBoard():
	Data = pd.read_csv("Data.csv")
	Data = Data.sample(frac=1).reset_index(drop=True)
	print(Data)
	return render_template("TextBoard.html",Data=Data)


app.run(debug=True, host='0.0.0.0', port=3000)
#要注意port要改

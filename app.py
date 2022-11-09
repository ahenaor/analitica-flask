from flask import Flask, render_template, request, redirect, url_for, send_from_directory

import os
from decouple import config
import json
import pyodbc

app = Flask(__name__)

def connDB(data):
	

	cnxn = pyodbc.connect(config('SQLAZURECONNSTR'))

	cursor = cnxn.cursor()
	
	sql = 	"""
			INSERT INTO dbo.Flask01 (primerInput) 
			VALUES (?) 
			"""
	jsonData = {}
	jsonData["primerInput"] = data


	cursor.execute(sql, json.dumps(jsonData))
	
	
	cursor.commit() 
	cnxn.close()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
		'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
	name = request.form.get('name')

	if name:
		print('Request for hello page received with name=%s' % name)

		connDB(name)

		return render_template('hello.html', name = name)
	else:
		print('Request for hello page received with no name or blank name -- redirecting')
		return redirect(url_for('index'))


if __name__ == '__main__':
	app.run()

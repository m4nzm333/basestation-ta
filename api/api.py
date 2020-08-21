from flask import Flask, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
import os
# import random
from gpiozero import CPUTemperature
import psutil
from datetime import datetime
import sqlite3

import sys
sys.path.append(".")
from SqlMonitor import SqlMonitor

UPLOAD_FOLDER = './data/post'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return render_template("welcome.html")


@app.route('/api', methods=['POST'])
def getFiles():
    # Check if file not exist in POST request
    if 'file' not in request.files:
        return jsonify({'response':'error', 'message':'Field file not found!'})
    file = request.files['file']
    # Check if filename is empty
    if file.filename == '':
        return jsonify({'response':'error', 'message':'Filename is empty!'})
    # Check if file is allowed extension
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'response':'success', 'message':'Upload success!'})
    else:
        return jsonify({'response':'error', 'message':'File extension denied!'})

@app.route('/getStatus', methods=['GET'])
def getStatus():
    cpu = CPUTemperature()
    now = datetime.now()
    memory = dict(psutil.virtual_memory()._asdict())
    return jsonify(
        {
            'cpu' : {
                'temp' : str(round(cpu.temperature, 2)),
                'utilize' : str(psutil.cpu_percent())
            },
            'memory' : {
                'percent' : str(memory['percent']),
                'used' : str(memory['used']),
                'total' : str(memory['total'])
            },
            'datetime' : str(now)
        }
    )

@app.route('/getLast50rows', methods=['GET'])
def getLast50Rows():
    data = SqlMonitor.getQuery('SELECT sensorTime, value FROM (SELECT sensorTime, value FROM temperature WHERE id = "cd14" ORDER BY sensorTime DESC LIMIT 100) ORDER BY sensorTime')
    return jsonify(data)

app.run('192.168.200.1', port=8080, debug=True)
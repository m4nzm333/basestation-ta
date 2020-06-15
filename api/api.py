from flask import Flask, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
import os
# For Random
import random

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
    # TODO : Get CPU Temp Value and Memory Load
    return jsonify({'cpuTemp': random.randint(30,50), 'memoryLoad': random.randint(300,500)})

app.run('0.0.0.0', 80, debug=True)
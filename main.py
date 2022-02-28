from flask import Flask,request,render_template,redirect
from prediction import Prediction
import pandas as pd
from trainModel import Train
from appLogger.app_logger import AppLogger
logger=AppLogger()
app=Flask(__name__)

@app.route('/')
def run():
    return render_template('index.html',training='')
@app.route('/train',methods=['POST','GET'])
def train():
    try:
        obj = Train()
        obj.startTraining()
        return render_template('index.html',training='Model training Completed')
    except Exception as e:
        logger.logger(str(e))
        return str(e)

@app.route('/predict',methods=['POST','GET'])
def predict():
    try:
        filepath = request.form['file']
        data = pd.read_csv(filepath)
        pred = Prediction()
        result = pred.predict(data)
        return render_template('prediction.html',result = result)
    except Exception as e:
        logger.logger(str(e))
        return str(e)

@app.route('/visualize',methods=["POST","GET"])
def visualize():
    try:
        return render_template('report.csv')
    except Exception as e:
        logger.logger(str(e))

@app.route('/logs',methods=['GET','POST'])
def logs():
    try:
        with open("logFiles\logfiles.txt", "r") as f:
            result = f.readlines()
        print(result)
        return render_template('logFiles.html',result=result)
    except Exception as e:
        logger.logger(str(e))
if '__main__'==__name__:
    app.run(port=8000)
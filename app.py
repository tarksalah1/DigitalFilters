from flask import Flask, render_template, request, jsonify
import pandas as pd
from scipy import signal as sig
import math 
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')
	
# @app.route('/upload', methods = ['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':

#     return render_template('index.html')
        
@app.route('/plot', methods = ['GET', 'POST'])
def digital_filter_data():
    url = "https://raw.githubusercontent.com/MohamedMostafa23/Digital-Filter/main/Data-Nor-ECG.csv"
    data_url = requests.get(url).content
    Xaxis_data = pd.read_csv(io.StringIO(data_url.decode('utf-8'))).iloc[:, 0].tolist()
    Yaxis_data = pd.read_csv(io.StringIO(data_url.decode('utf-8'))).iloc[:, 1].tolist()
    Filtered_data = []
    zeros = []
    poles = []
    zero = 0
    pole = 0
    if request.method == 'POST':
        data = request.json
        for index in range(len(data)):
            if data[index]['type'] == "nonConjZero" or data[index]['type'] == "ConjZero":
                zero = complex(data[index]['point'][0],data[index]['point'][1])
                zeros.append(zero)

        for index in range(len(data)):
            if data[index]['type'] == "nonConjPole" or data[index]['type'] == "ConjPole":
                pole = complex(data[index]['point'][0],data[index]['point'][1])
                poles.append(pole)

    sysDnum, sysDden = sig.zpk2tf(zeros, poles, 1)
    print(sysDnum)
    print(sysDden)
    filtered_data_withComplex = sig.lfilter(sysDnum, sysDden, Yaxis_data)
    print(filtered_data_withComplex)
    for index in range(len(filtered_data_withComplex)):
        absolute = abs(filtered_data_withComplex[index])
        Filtered_data.append(absolute)

    data = jsonify({"data_Xaxis": Xaxis_data, "non_Filtered_Data" : Yaxis_data, "Filtered_Data" : Filtered_data})

    return data

if __name__ == '__main__':
    
    app.run(debug=True)

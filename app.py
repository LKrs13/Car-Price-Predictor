import re
from flask import Flask, render_template, request
import pickle
import requests
import numpy as np
import pandas as pd


model = pd.read_pickle(r'predictor/price/vehicles/file.pkl')

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')

@app.route("/predict", methods = ['GET', 'POST'])
def predict():
    if request.method == 'POST': 
        year = int(request.form["year"]) # taking year input from the user
        tot_year = 2020 - year
        present_price = float(request.form["msrp"]) #taking the present prize
        fuel_type = request.form["fuel"] # type of fuel of car
        # assigning numerical values
        if fuel_type == "Petrol":
            fuel = 2
        elif fuel_type == "Diesel":
            fuel= 1
        else:
            fuel = 0
        kms_driven = int(request.form["kms"]) # total driven kilometers of the car
        transmission = request.form["transmission"] # transmission type
        # assigning numerical values
        if transmission == "Manual":
            transmission_type = 1
        else:
            transmission_type = 0
        seller_type = request.form["seller"] # seller type
        if seller_type == "Individual":
            seller_individual = 1
        else:
            seller_individual = 0
        owner = int(request.form["owner"])  # number of owners
        # values = [['Age', 'Present_Price', 'Kms_Driven', 'Fuel_Type', 'Seller_Type', 'Transmission', 'Owner']]
        values = [[
        tot_year,
        present_price,
        kms_driven,
        fuel,
        seller_individual,
        transmission_type,
        owner,
        ]]
        # created a list of all the user inputed values, then using it for prediction
        prediction = model.predict(values)
        prediction = round(prediction[0],2)
        # returning the predicted value inorder to display in the front end web application
        return render_template("home.html", predPrice = '${prediction}!'.format(prediction=prediction))
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

import numpy as np
import pandas as pd
import pickle
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Load Model and Scaler
model = pickle.load(open("rdf.pkl", "rb"))
scaler = pickle.load(open("scale1.pkl", "rb"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict")
def predict():
    return render_template("input.html")


@app.route("/submit", methods=["POST"])
def submit():

    try:
        # Read Form Values
        Gender = float(request.form["Gender"])
        Married = float(request.form["Married"])
        Dependents = float(request.form["Dependents"])
        Education = float(request.form["Education"])
        Self_Employed = float(request.form["Self_Employed"])
        ApplicantIncome = float(request.form["ApplicantIncome"])
        CoapplicantIncome = float(request.form["CoapplicantIncome"])
        LoanAmount = float(request.form["LoanAmount"])
        Loan_Amount_Term = float(request.form["Loan_Amount_Term"])
        Credit_History = float(request.form["Credit_History"])
        Property_Area = float(request.form["Property_Area"])

        # Original Features
        features = [[
            Gender,
            Married,
            Dependents,
            Education,
            Self_Employed,
            ApplicantIncome,
            CoapplicantIncome,
            LoanAmount,
            Loan_Amount_Term,
            Credit_History,
            Property_Area
        ]]

        print("\n==============================")
        print("Original Features")
        print(features)

        # Scale
        scaled = scaler.transform(features)

        print("\nScaled Features")
        print(scaled)

        # DataFrame
        data = pd.DataFrame(scaled, columns=[
            "Gender",
            "Married",
            "Dependents",
            "Education",
            "Self_Employed",
            "ApplicantIncome",
            "CoapplicantIncome",
            "LoanAmount",
            "Loan_Amount_Term",
            "Credit_History",
            "Property_Area"
        ])

        print("\nDataFrame")
        print(data)

        # Prediction
        prediction = model.predict(data)

        print("\nPrediction =", prediction)

        if prediction[0] == 1:
            result = "✅ Loan Approved"
        else:
            result = "❌ Loan Rejected"

        return render_template("output.html", result=result)

    except Exception as e:
        return f"<h2>Error:</h2><pre>{e}</pre>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
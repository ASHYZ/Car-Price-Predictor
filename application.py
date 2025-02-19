from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("LinearRegressionModel.pkl", 'rb'))
car = pd.read_csv("Cleaned Car.csv")

@app.route('/')
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    years = sorted(car['year'].unique(), reverse=True)
    fuel_types = car['fuel_type'].unique()
    companies.insert(0,"Select Company")
    return render_template('index.html', companies=companies, car_models=car_models, years=years, fuel_types=fuel_types)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        company = request.form.get('company')
        car_model = request.form.get('car_model')
        year = int(request.form.get('year'))
        fuel_type = request.form.get('fuel_type')
        kms_driven = int(request.form.get('kilo_driven'))

        print(f"Company: {company}, Model: {car_model}, Year: {year}, Fuel Type: {fuel_type}, KMs Driven: {kms_driven}")

        # Perform prediction logic here
        input_df = pd.DataFrame([[car_model, company, year, kms_driven, fuel_type]], 
                                columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
        
        prediction = model.predict(input_df)

        return str(np.round(prediction[0],2))
    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Error predicting price", 500

if __name__ == "__main__":
    app.run(debug=True)

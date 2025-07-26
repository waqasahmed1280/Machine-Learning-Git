from flask import Flask, render_template, request
import pandas as pd
import pickle

# Load the model pipeline
model_pipeline = pickle.load(open('pipeline.pkl', 'rb'))

app = Flask(__name__)


def predict_car_price(model_pipeline, year, kilometers_driven, fuel_type, transmission, owner_type, seats, mileage, engine, power):
    input_data = pd.DataFrame({
        'Year': [year],
        'Kilometers_Driven': [kilometers_driven],
        'Fuel_Type': [fuel_type],
        'Transmission': [transmission],
        'Owner_Type': [owner_type],
        'Seats': [seats],
        'Mileage': [mileage],
        'Engine': [engine],
        'Power': [power]
    })
    prediction = model_pipeline.predict(input_data)
    return prediction[0]


@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_price = None
    if request.method == 'POST':
        year = int(request.form['year'])
        kilometers_driven = int(request.form['kilometers_driven'])
        fuel_type = request.form['fuel_type']
        transmission = request.form['transmission']
        owner_type = request.form['owner_type']
        seats = float(request.form['seats'])
        mileage = float(request.form['mileage'])
        engine = int(request.form['engine'])
        power = float(request.form['power'])

        predicted_price = predict_car_price(
            model_pipeline,
            year,
            kilometers_driven,
            fuel_type,
            transmission,
            owner_type,
            seats,
            mileage,
            engine,
            power
        )

    return render_template('index.html', predicted_price=predicted_price)



if __name__ == '__main__':
    app.run(debug=True)

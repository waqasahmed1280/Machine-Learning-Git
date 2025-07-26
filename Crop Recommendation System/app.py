from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load('crop_model.pkl')

# Crop mapping
crop_dict = {
    1: 'rice', 2: 'maize', 3: 'jute', 4: 'cotton', 5: 'coconut', 6: 'papaya',
    7: 'orange', 8: 'apple', 9: 'muskmelon', 10: 'watermelon', 11: 'grapes',
    12: 'mango', 13: 'banana', 14: 'pomegranate', 15: 'lentil', 16: 'blackgram',
    17: 'mungbean', 18: 'mothbeans', 19: 'pigeonpeas', 20: 'kidneybeans',
    21: 'chickpea', 22: 'coffee'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form inputs
        features = [float(request.form[i]) for i in ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'Ph', 'Rainfall']]
        prediction = model.predict(np.array([features]))[0]
        crop = crop_dict.get(prediction, "Unknown")
        return render_template('index.html', prediction_text=f"{crop}")

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {e}")
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/eval')
def eval():
    return render_template('eval.html')  # create this template or replace with valid page

@app.route('/overall')
def evaluate():
    return render_template('overall.html')

if __name__ == "__main__":
    app.run(debug=True)

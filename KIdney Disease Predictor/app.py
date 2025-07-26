from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load model and scaler
scaler = pickle.load(open("models/scaler.pkl", 'rb'))
model_gbc = pickle.load(open("models/model_gbc.pkl", 'rb'))

def predict_ckd(data):
    df = pd.DataFrame([data])

    # Convert categorical values
    df['htn'] = 1 if data['htn'] == 'yes' else 0
    df['dm'] = 1 if data['dm'] == 'yes' else 0
    df['cad'] = 1 if data['cad'] == 'yes' else 0
    df['appet'] = 1 if data['appet'] == 'good' else 0
    df['pc'] = 1 if data['pc'] == 'normal' else 0

    # Scale numeric values
    numeric_cols = ['age', 'bp', 'sg', 'al', 'hemo', 'sc']
    df[numeric_cols] = scaler.transform(df[numeric_cols])

    # Predict
    prediction = model_gbc.predict(df)[0]
    return prediction

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        form = request.form
        data = {
            "age": float(form["age"]),
            "bp": float(form["bp"]),
            "sg": float(form["sg"]),
            "al": float(form["al"]),
            "hemo": float(form["hemo"]),
            "sc": float(form["sc"]),
            "htn": form["htn"],
            "dm": form["dm"],
            "cad": form["cad"],
            "appet": form["appet"],
            "pc": form["pc"]
        }
        result = predict_ckd(data)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# Load dataset and model
data = pd.read_csv('cleaned_data.csv')
pipe = pickle.load(open("RidgeModel.pkl", "rb"))

@app.route('/')
def index():
    locations = sorted(data['location'].unique())
    return render_template('index.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    bhk = request.form.get('bhk')
    bath = request.form.get('bath')
    sqft = request.form.get('total_sqft')

    # Convert input into dataframe
    input_df = pd.DataFrame([[location, float(sqft), float(bath), float(bhk)]],
                            columns=['location', 'total_sqft', 'bath', 'bhk'])

    prediction = pipe.predict(input_df)[0] * 1e5
    return str(np.round(prediction, 2))

if __name__ == "__main__":
    app.run(debug=True, port=5001)

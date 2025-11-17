import os
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for
from pycaret.classification import load_model, predict_model

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model
# This assumes 'diabetes_model.pkl' is in the same directory
try:
    model = load_model('diabetes_model')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Define the home route
@app.route('/')
def home():
    # Render the HTML form
    return render_template('index.html')

# Define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return "Error: Model not loaded.", 500

    try:
        # Get data from the HTML form
        data = {
            'Number of times pregnant': [int(request.form['pregnant'])],
            'Plasma glucose concentration a 2 hours in an oral glucose tolerance test': [int(request.form['glucose'])],
            'Diastolic blood pressure (mm Hg)': [int(request.form['bp'])],
            'Triceps skin fold thickness (mm)': [int(request.form['skin'])],
            '2-Hour serum insulin (mu U/ml)': [int(request.form['insulin'])],
            'Body mass index (weight in kg/(height in m)^2)': [float(request.form['bmi'])],
            'Diabetes pedigree function': [float(request.form['pedigree'])],
            'Age (years)': [int(request.form['age'])]
        }
        
        # Create a Pandas DataFrame
        input_df = pd.DataFrame.from_dict(data)
        
        print(f"Input data for prediction: \n{input_df}")

        # Make predictions
        prediction = predict_model(model, data=input_df)
        
        # Get the 'Label' from the prediction (1 = Diabetes, 0 = No Diabetes)
        output = prediction['Label'].iloc[0]
        
        result_text = "High Risk of Diabetes" if output == 1 else "Low Risk of Diabetes"

        print(f"Prediction: {output} -> {result_text}")
        
        # Pass the result back to the HTML page
        return render_template('index.html', prediction_text=f'Prediction: {result_text}')

    except Exception as e:
        print(f"Prediction error: {e}")
        return render_template('index.html', prediction_text=f'Error: {e}')

if __name__ == '__main__':
    # HuggingFace Spaces sets the PORT environment variable
    # We use 7860 as a default if PORT isn't set
    port = int(os.environ.get("PORT", 7860))
    # We must host on 0.0.0.0 to make it accessible in Docker
    app.run(host='0.0.0.0', port=port)
from flask import Flask, render_template, request, redirect, url_for
from utils import load_saved_artifacts, process_and_predict
import sys

app = Flask(__name__)

# --- LOAD MODEL ARTIFACTS ---
try:
    model, encoders, features = load_saved_artifacts()
    print("SUCCESS: Model and Artifacts loaded successfully.")
except Exception as e:
    print(f"FATAL ERROR: Could not load model files. {e}")
    sys.exit(1)

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # 1. Collect form data from index.html
        form_data = request.form.to_dict()
        
        try:
            # 2. Get prediction (e.g., 'Approved' or 'Rejected')
            prediction_result = process_and_predict(form_data, model, encoders, features)
            
            # 3. Send the user to the SEPARATE result page (predict.html)
            return render_template('predict.html', prediction=prediction_result)
            
        except Exception as e:
            # If something goes wrong, show the error on the index page
            return render_template('index.html', error=str(e))
    
    # Normal GET request: Show the landing page
    return render_template('index.html')

if __name__ == '__main__':
    # Run the server
    app.run(debug=True, port=9000)

     
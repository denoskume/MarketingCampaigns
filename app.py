from flask import Flask, request, jsonify
import joblib
import pandas as pd
import xgboost as xgb

# Load the saved model
model = joblib.load('best_model.pkl')

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Convert JSON data to DataFrame
        df = pd.DataFrame(data)
        
        # Create DMatrix for prediction
        dmatrix = xgb.DMatrix(df)
        
        # Make predictions
        predictions = model.predict(dmatrix)
        predictions_binary = [1 if pred > 0.5 else 0 for pred in predictions]
        
        # Return predictions as JSON
        return jsonify(predictions_binary)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

from datetime import datetime
import os
import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

# Load and save the model
model = joblib.load("./BackEnd/Models/SoftMax/softmax_model.pkl")
vectorizer = joblib.load("./BackEnd/Models/SoftMax/softmax_vectorizer.pkl")
    
# Define Flask app and use CORS
app = Flask(__name__)
CORS(app)

# Handle POST API requests
@app.route("/api/predict_news", methods=["POST"])
def predict_news():
    # Receive data from the client
    news_data = request.json
    news_text = news_data["news_text"]
    news_tfidf = vectorizer.transform([news_text])

    # Predict probabilities for each class
    probabilities = model.predict_proba(news_tfidf)[0]
    # Get the index of the class with the highest probability
    predicted_class = model.predict(news_tfidf)[0]

    # Return the result as JSON
    if predicted_class == 1:
        return jsonify({"prediction": "fake", "probability": probabilities[1]})
    else:
        return jsonify({"prediction": "true", "probability": probabilities[0]})


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

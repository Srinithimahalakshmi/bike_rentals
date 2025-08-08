from flask import Flask, render_template, jsonify
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import joblib
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Load dataset
    df = pd.read_csv("data/day.csv")

    # Select numeric features
    features = df.select_dtypes(include=['int64', 'float64']).drop(columns=['instant', 'casual', 'registered', 'cnt'], errors='ignore')
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Save model
    os.makedirs("model", exist_ok=True)
    joblib.dump(pca, "model/pca_model.joblib")

    # Prepare JSON data
    data = [{"x": float(x), "y": float(y)} for x, y in X_pca]

    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)

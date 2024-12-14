from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.cluster import KMeans

app = Flask(__name__)

# Example data: Crime incidents with geolocation (latitude, longitude) and severity level
data = {
    "latitude": [37.7749, 37.7840, 37.7640, 37.7849],
    "longitude": [-122.4194, -122.4094, -122.4294, -122.4195],
    "severity": [3, 4, 2, 5]  # 1: Low, 5: High
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# API endpoint: Fetch safety data
@app.route('/api/safety-data', methods=['GET'])
def get_safety_data():
    # Apply clustering to identify high-risk areas
    kmeans = KMeans(n_clusters=2, random_state=0).fit(df[['latitude', 'longitude']])
    df['cluster'] = kmeans.labels_

    # Create safety scores (example logic)
    df['safety_score'] = df['severity'].apply(lambda x: 5 - x)  # High severity -> Low safety score

    return jsonify(df.to_dict(orient='records'))

# API endpoint: Submit user feedback
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    feedback = request.json
    new_entry = {
        "latitude": feedback['latitude'],
        "longitude": feedback['longitude'],
        "severity": feedback['severity']
    }
    df.loc[len(df)] = new_entry
    return jsonify({"message": "Feedback submitted successfully!"}), 201

# Serve frontend
@app.route('/')
def index():
    return render_template('index.html')  # Frontend will go in 'templates/index.html'

if __name__ == '__main__':
    app.run(debug=True)

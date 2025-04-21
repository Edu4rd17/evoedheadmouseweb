from flask import Flask, Response, jsonify
from flask_cors import CORS
from webcam_stream import liveFaceRecognitionTracking
import cv2
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://evoedheadmouseweb.vercel.app"}})

# Open the webcam at startup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    raise RuntimeError("Cannot open webcam.")

@app.route('/')
def home():
    return jsonify({"message": "Backend is working now EDIIII!"})

@app.route('/video_feed')
def video_feed():
    return Response(liveFaceRecognitionTracking(cap), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Heroku sets PORT; fallback to 5000 for local dev
    app.run(debug=False, host='0.0.0.0', port=port)

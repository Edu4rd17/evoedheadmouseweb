from flask import Flask, Response, jsonify
from flask_cors import CORS
from webcam_stream import liveFaceRecognitionTracking
import cv2

app = Flask(__name__)
CORS(app)

# Open the webcam at startup
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use CAP_DSHOW on Windows for faster init
# if not cap.isOpened():
#     raise RuntimeError("Cannot open webcam.")

@app.route('/')
def home():
    return jsonify({"message": "Backend is working now EDIIII!"})

# @app.route('/video_feed')
# def video_feed():
#     return Response(liveFaceRecognitionTracking(cap), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

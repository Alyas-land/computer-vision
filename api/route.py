from flask import jsonify, request, Response
from flask.views import MethodView
import cv2
import threading

status = "NO_FACE"
last_frame = None

# Load Haar Cascade
human_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

def camera_thread():
    global status, last_frame
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        humans = human_cascade.detectMultiScale(gray, 1.1, 4)

        if len(humans) > 0:
            status = "FACE"
        else:
            status = "NO_FACE"

        for (x, y, w, h) in humans:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        last_frame = frame

# Thread starts automatically when this module is imported
threading.Thread(target=camera_thread, daemon=True).start()


def generate_frames():
    global last_frame
    while True:
        if last_frame is None:
            continue
        ret, buffer = cv2.imencode('.jpg', last_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


class SendData(MethodView):
     
     def get(self):
        print('yes')
        print(status)
        return jsonify({"status": status})
     
    #  def post(self):
    #     return jsonify({"status": status})
     

class VideoFeed(MethodView):
    def get(self):
        return Response(generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
        



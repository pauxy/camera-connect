import threading
import server
from flask import Flask,render_template,Response
import cv2

app=Flask(__name__)
ser =server.server("",8089)

def generate_frames():
    while True:
        # Capture frame-by-frame
        frame = ser.FRAME  # read the camera frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    print("hello")
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5004, debug=True, use_reloader=False)).start()
    ser.start()

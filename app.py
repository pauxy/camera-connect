import threading
import server
from flask import Flask,render_template,Response
import cv2
import sys

app=Flask(__name__)
ser =server.server("",int(sys.argv[1]))
ser2 = server.server("",int(sys.argv[2]))

def generate_frames(ser):
    while True:
        # Capture frame-by-frame
        frame = ser.FRAME  # read the camera frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/v1')
def video():
    return Response(generate_frames(ser),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/v2')
def video2():
    return Response(generate_frames(ser2),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    print("hello")
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5004, debug=True, use_reloader=False)).start()
    ser.start()

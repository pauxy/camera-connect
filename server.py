import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import threading

class server():
    HOST=''
    PORT=8089
    FRAME = None
    
   
    def __init__(self):
        pass

    def start(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #print 'Socket created'

        s.bind((self.HOST,self.PORT))
        #print 'Socket bind complete'
        s.listen(10)
        #print 'Socket now listening'

        conn,addr=s.accept()

        ### new
        data = conn.recv(1)
        payload_size = struct.calcsize("L") 
        while True:
            while len(data) < payload_size:
                data += conn.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            ###
            #print(frame_data)
            #print(type(frame_data))
            #loaded_np = np.load(frame_data, allow_pickle=True)
            threading.Thread(target=self.frameSet,args=(frame_data,)).start()

    def frameSet(self,frame_data):
        self.FRAME = pickle.loads(frame_data)
    

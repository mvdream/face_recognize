from django.shortcuts import render,HttpResponse
from django.views import View,generic
from faceapp import face_detector,addstudent
import numpy as np,pandas as pd,cv2,os,base64,json
from io import BytesIO,StringIO
from PIL import Image, ImageDraw
from faceapp.spoofing_detector import detect_spoof
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

class Home(View):
    def get(self,request):
        return render(request,"faceapp/index.html")

class FaceRecognize(View):

    def post(self,request):
        img = request.POST.get('image')
        output_data = {'students':[],'status':'Successfully recognize students','error':False}
        response_data = []        
        if len(img)<10:
            output_data['error'] = True
            output_data['status'] = "No image"
            response_data.append(output_data)
            return HttpResponse(json.dumps(response_data))
        img = base64.b64decode(img[23:])
        img = np.array(Image.open(BytesIO(img)))
        data = face_detector.predict(img)
        names = []
        if data['error']:
            response_data.append(data)
            return HttpResponse(json.dumps(response_data))
        for name,(top, right, bottom, left) in data['students']:
            faces = {}
            face = img[top:bottom,left:right]
            faces['fake'] = True if detect_spoof(face) else False
            faces['name'] = name
            names.append(faces)
        data['students'] = names
        response_data.append(data)
        return HttpResponse(json.dumps(response_data))

class AddStudent(View):

    def post(self,request):
        encode_img = request.POST.get('image')
        name = request.POST.get('name')
        print(name)
        img = base64.b64decode(encode_img)
        img = np.array(Image.open(BytesIO(img)))
        status = addstudent.add_new(name,img)
        return HttpResponse(json.dumps([{'status':status}]))

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        print("dss")
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass


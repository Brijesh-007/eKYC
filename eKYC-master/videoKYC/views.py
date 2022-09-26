import re
from itertools import count
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from matplotlib.pyplot import flag

import numpy as np
# import urllib # python 2
import urllib.request # python 3
import json
import cv2
import os

from .camera import VideoCamera

# Create your views here.

def home(request):
    return render(request, 'form.html')

def video(request):
	return render(request, 'video.html')

def gen(camera):
	flag = True
	while True:
		frame, flag = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		if not flag:
			break
	return redirect("/last")
	

#Method for laptop camera
def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace ;boundary=frame')

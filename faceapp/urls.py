from django.urls import path,include
from .views import *
from faceapp import views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    # path('facedetect/',FaceRecognize.as_view(), name='detect'),
    # path('video/',views.livefe, name='detect'),
    path('video/',Home.as_view(), name='home'),
    path('image/',FaceRecognize.as_view(), name='detect'),

]
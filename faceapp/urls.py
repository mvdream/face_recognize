from django.urls import path,include
from .views import *
from faceapp import views
from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('',Home.as_view(), name='home'),
    path('add/',AddStudent.as_view(), name='add'),
    path('scan/',ScanPeople.as_view(), name='scan'),
    path('scan/recognize/',csrf_exempt(FaceRecognize.as_view()), name='recognize'),

]
from django.urls import path
from .views import *

urlpatterns = [
    path('excelFile/', FileUploadView.as_view()),
    path('lpc/',LPCDownloadView),
    path('pc/',PCDownloadView),
    path('plasmalogen/',PlasmalogenDownloadView),
    path('roundoff/',RoundDownloadView),
    path('mean/',MeanDownloadView),

    
]
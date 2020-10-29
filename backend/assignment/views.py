from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import pandas as pd
from .models import File as excelFile
from .models import TaskResult as taskResult
from rest_framework import viewsets 
from .serializers import FileSerializer
from rest_framework import views
from rest_framework.response import Response
from django.conf import settings
from backend.settings import MEDIA_ROOT
import os

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)
    def post(self, request, *args, **kwargs):
      file_serializer = FileSerializer(data=request.data)
      
      if file_serializer.is_valid():
          file_serializer.save()

          file_obj = excelFile.objects.all().order_by('-id')[0]
          excel = file_obj.id
          print(excel)
          excel = file_obj.file.read()
          data_1 = pd.read_excel(excel)    
          data_1 = data_1.dropna()
          
          Acceptence = data_1['Accepted Compound ID']
          index_PC = Acceptence.str.endswith('PC')
          index_LPC = Acceptence.str.endswith('LPC')
          index_plasmalogen = Acceptence.str.endswith('plasmalogen')
          #   task 1
          data_LPC = data_1.loc[index_LPC]
          GDRAT_abs_path = os.path.join(MEDIA_ROOT + '/LPC.xlsx')
          data_LPC.to_excel(GDRAT_abs_path, index = False, header=True)
          data_PC = data_1.loc[index_PC]
          GDRAT_abs_path = os.path.join(MEDIA_ROOT + '/PC.xlsx')
          data_PC.to_excel(GDRAT_abs_path, index = False, header=True)
          data_plasmogen = data_1.loc[index_plasmalogen]
          GDRAT_abs_path = os.path.join(MEDIA_ROOT + '/PLASMA.xlsx')
          data_plasmogen.to_excel(GDRAT_abs_path, index = False, header=True)
          #   task 2   
          data_1['Retention Time Roundoff (in mins)']  = data_1.round({'Retention time (min)':0})['Retention time (min)']
          data_1['Retention Time Roundoff (in mins)'].value_counts()
          GDRAT_abs_path = os.path.join(MEDIA_ROOT + '/task2.xlsx')
          data_1.to_excel(GDRAT_abs_path, index = False, header=True)

          #   task3  
          task_3_data = data_1.drop(['m/z', 'Retention time (min)', 'Accepted Compound ID',], axis=1) 
          mean_dataframe= task_3_data.groupby(task_3_data['Retention Time Roundoff (in mins)'])
          mean_dataframe = mean_dataframe.mean()
          mean_dataframe = mean_dataframe.reset_index()
          GDRAT_abs_path = os.path.join(MEDIA_ROOT + '/task3.xlsx')
          mean_dataframe.to_excel(GDRAT_abs_path, index = False, header=True)

          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import HttpResponse
from wsgiref.util import FileWrapper

def LPCDownloadView(request):
    file_obj = os.path.join(MEDIA_ROOT + '/LPC.xlsx')
    document = open(file_obj, 'rb')   
    response = HttpResponse(FileWrapper(document),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="LPC.xlsx"'

    return response

def PCDownloadView(request):
    file_obj = os.path.join(MEDIA_ROOT + '/PC.xlsx')
    document = open(file_obj, 'rb')   
    response = HttpResponse(FileWrapper(document),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="PC.xlsx"'

    return response


def PlasmalogenDownloadView(request):
    file_obj = os.path.join(MEDIA_ROOT + '/PLASMA.xlsx')
    document = open(file_obj, 'rb')   
    response = HttpResponse(FileWrapper(document),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="plasmalogen.xlsx"'
    return response

def RoundDownloadView(request):
    file_obj = os.path.join(MEDIA_ROOT + '/task2.xlsx')
    document = open(file_obj, 'rb')   
    response = HttpResponse(FileWrapper(document),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="roundoff.xlsx"'
    return response


def MeanDownloadView(request):
    file_obj = os.path.join(MEDIA_ROOT + '/task3.xlsx')
    document = open(file_obj, 'rb')   
    response = HttpResponse(FileWrapper(document),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="mean.xlsx"'
    return response


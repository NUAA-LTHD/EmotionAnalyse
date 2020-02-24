import os
from django.shortcuts import render
from index.models import emotion
from django.http import HttpResponse
import datetime
def register(request):
    if request.method=="GET":
        receive_data=request.GET
        username=receive_data['username']
        password=receive_data['password']
        data=emotion()
        data.username=username
        data.password=password
        data.register_date=datetime.datetime.now()
        data.save()
        return HttpResponse("success")
def login(request):
    if request.method=="GET":
        receive_data=request.GET
        username=receive_data['username']
        password=receive_data['password']
        response = emotion.objects.filter(username=username)
        if not response.exists():
            return HttpResponse("failed")
        response=list(response)
        if response[0].password != password:
            return HttpResponse("failed")
        return HttpResponse("success")
def doc(request,title):
    file_name=title+".html"
    if os.path.exists(".//templates//"+file_name):
        return render(request,file_name)
    else:
        context=dict()
        context['message']="抱歉，没有找到您要的文档"
        return render(request,"404.html",context)
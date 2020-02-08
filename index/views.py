import os
from django.shortcuts import render
def doc(request,title):
    file_name=title+".html"
    if os.path.exists(".//templates//"+file_name):
        return render(request,file_name)
    else:
        context=dict()
        context['message']="抱歉，没有找到您要的文档"
        return render(request,"404.html",context)
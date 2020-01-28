import os
from django.shortcuts import render
def doc(request,title):
    file_name=title+".html"
    if os.path.exists(".//templates//"+file_name):
        return render(request,file_name)
    else:
        return render(request,"404.html")

from django.shortcuts import render
def not_found(request,exception):
    context=dict()
    context['message']="咦，木有找到您要的页面"
    return render(request,"404.html",context)
from django.shortcuts import render
def not_found(request,exception):
    context=dict()
    context['message']="页面迷失在海洋中..."
    return render(request,"404.html",context)
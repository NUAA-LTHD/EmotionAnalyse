import os
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from login.models import users
def doc(request, title):
    # TODO:doc返回404js仍然无法加载
    file_name = title + ".html"
    if os.path.exists(".//templates//" + file_name):
        return render(request, file_name)
    else:
        context = dict()
        context['message'] = "抱歉，没有找到您要的文档"
        return render(request, "404.html", context)


def index(request):
    session = request.session
    if 'user_id' in session:
        user_id=session['user_id']
        response = users.objects.filter(id=user_id)
        nickname=response[0].nickname
        contex=dict()
        contex['nickname'] = nickname
        return render(request, "index.html", contex)
    else:
        session['tip'] = "您还未登陆，请先登陆"
        return HttpResponseRedirect("/login")
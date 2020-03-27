import os
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from login.models import Users
from blog.models import Article
from DjangoUeditor.forms import UEditorField
from django import forms
from django.forms import widgets
import datetime
class DjangoueditorForm(forms.Form):
    title=forms.CharField(label='题目',min_length=1)
    content = UEditorField(\
        "", initial="", width=800, height=200, \
        toolbars = 'full',\
        imagePath = 'images/{}/'.format(datetime.datetime.now().strftime("%Y-%m")),\
        filePath = 'files/{}/'.format(datetime.datetime.now().strftime("%Y-%m")),
        upload_settings={"imageMaxSize":10240000},)

def doc(request, title):
    file_name = title + ".html"
    if os.path.exists(".//templates//" + file_name):
        return render(request, file_name)
    else:
        context = dict()
        context['err_msg'] = "你要的文档已经迷失在浩瀚的大海..."
        return render(request, "404.html", context)


def index(request):
    session = request.session
    if 'user_id' in session:
        user_id=session['user_id']
        response = Users.objects.filter(id=user_id)
        nickname=response[0].nickname
        contex=dict()
        contex['nickname'] = nickname
        return render(request, "index.html", contex)
    else:
        session['tip'] = "您还未登陆，请先登陆"
        return HttpResponseRedirect("/login")

def write(request):
    session = request.session
    if 'user_id' in session:
        if request.method=='GET':
            user_id = session['user_id']
            response = Users.objects.filter(id=user_id)
            nickname = response[0].nickname
            contex = dict()
            contex['nickname'] = nickname
            contex['forms']=DjangoueditorForm()
            return render(request, "write.html", contex)
        else:#如果是post
            data=request.POST
            user_id = session['user_id']
            auth = Users.objects.filter(id=user_id)
            article=Article()
            article.title=data.get('title')
            article.auth=auth[0]
            article.content=data.get('content')
            article.save()
            url="../view?id={}".format(article.id)
            return HttpResponseRedirect(url)
    else:
        session['tip'] = "您还未登陆，请先登陆"
        return HttpResponseRedirect("/login")
def view(request):
    session = request.session
    if 'user_id' in session:
        if request.method == 'GET':
            data=request.GET
            id=data['id']
            article=Article.objects.filter(id=id)
            if article.exists():
                article=article[0]
                contex=dict()
                contex['title']=article.title
                contex['content']=article.content
                return render(request,"view.html",contex)
            else:
                return render(request,"404.html")
    else:
        session['tip'] = "您还未登陆，请先登陆"
        return HttpResponseRedirect("/login")
def mine(request):
    session = request.session
    if 'user_id' in session:
        auth=Users.objects.filter(id=session['user_id'])
        auth=auth[0]
        articles=auth.articles.all().order_by('-create_time')
        article_list=list()
        for article in articles:
            article_dict=dict()
            url="../view?id={}".format(article.id)
            title=article.title
            article_dict['url']=url
            article_dict['title']=title
            article_dict['date']=article.create_date_time
            article_list.append(article_dict)
        contex=dict()
        contex['article_list']=article_list
        return render(request,"mine.html",contex)


    else:
        session['tip'] = "您还未登陆，请先登陆"
        return HttpResponseRedirect("/login")
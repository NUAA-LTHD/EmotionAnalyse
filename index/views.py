import os
from django.shortcuts import render
from index.models import emotion
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from EmotionAnalyse import settings#为了节省代码没有重写读取ini文件的代码而是直接引入settings
import hashlib
from django.views.decorators.csrf import csrf_exempt
class Encrypt():
    def __init__(self):
        conf= settings.conf
        self.salt=conf.get("login","salt")
    def encrypt(self,str):
        str=self.salt+str+self.salt
        str= str.encode(encoding="utf-8")
        str=hashlib.md5(str).hexdigest()#密码加盐加密
        return str

# 因为不习惯使用自带的用户认证机制，所以自己重写了login，logout，register
def register(request):
    if request.method=="POST":
        contex=dict()
        receive_data=request.POST
        username=receive_data.get('username')
        nickname = receive_data.get('nickname')
        password = receive_data.get('password')
        if username==None or nickname == None or password ==None\
                or len(username)<5 or len(password) < 8 or len(nickname) <1 :
            return HttpResponse("数据不合法")
        print(username,nickname)
        contex['nickname'] = nickname
        contex['username'] = username
        response = emotion.objects.filter(nickname=nickname)
        if response.exists():  # 如果昵称已经存在
            contex['err_msg'] = "昵称已存在"
            return render(request, "register.html", contex)
        response = emotion.objects.filter(username=username)
        if response.exists():#如果用户名已经存在
            contex['err_msg']="用户名已存在"
            return render(request,"register.html",contex)
        password_encrypted=Encrypt().encrypt(password)
        data=emotion()
        data.username=username
        data.password=password_encrypted
        data.nickname=nickname
        data.register_date=datetime.datetime.now()
        print(password_encrypted,len(password_encrypted))
        data.save()#写入数据库
        return HttpResponseRedirect("/index/login")
    if request.method=="GET":
        return render(request,"register.html")
def login(request):
    if request.method=="POST":
        contex=dict()
        contex['err_msg']="用户名或密码错误"
        receive_data=request.POST
        username=receive_data.get('username')
        password = receive_data['password']
        if username==None or  password == None:
            return HttpResponse("我怀疑你视图攻击我，但是我没有证据")
        contex['username']=username
        response = emotion.objects.filter(username=username)
        if not response.exists():#用户不存在
            return render(request,"login.html",contex)
        password_encrypted=Encrypt().encrypt(password)
        response=list(response)
        if response[0].password != password_encrypted:#密码错误
            return render(request,"login.html",contex)
        session=request.session
        session['username']=username#设置session
        session['nickname']=response[0].nickname
        return HttpResponseRedirect("/index")
    if request.method=="GET":
        return render(request,"login.html")
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/index/login')
@csrf_exempt
def doc(request,title):
    #TODO:doc返回404js仍然无法加载
    file_name=title+".html"
    if os.path.exists(".//templates//"+file_name):
        return render(request,file_name)
    else:
        context=dict()
        context['message']="抱歉，没有找到您要的文档"
        return render(request,"404.html",context)
def index(request):
    session=request.session
    if 'username' in session:
        contex=dict()
        contex['username']=session['username']
        contex['nickname']=session['nickname']
        return render(request,"index.html",contex)
    else:
        return HttpResponseRedirect("/index/login")
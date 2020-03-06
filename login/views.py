import os
from django.shortcuts import render
from login.models import users
from api.models import email_record
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
import datetime
from EmotionAnalyse import settings  # 为了节省代码没有重写读取ini文件的代码而是直接引入settings
import hashlib
import time
# 因为不习惯使用自带的用户认证机制，所以自己重写了login，logout，register
def register(request):
    if request.method == "POST":
        username, password, nickname,email,verify_code = RegisterData(request).get_data()
        if username == None:
            return HttpResponse("数据不合法")
        contex = dict()
        contex['nickname'] = nickname
        contex['username'] = username
        contex['email']=email
        response = users.objects.filter(nickname=nickname)
        if response.exists():  # 如果昵称已经存在
            contex['err_msg'] = "昵称已存在"
            return render(request, "register.html", contex)
        response = users.objects.filter(username=username)
        if response.exists():  # 如果用户名已经存在
            contex['err_msg'] = "用户名已存在"
            return render(request, "register.html", contex)
        response = users.objects.filter(email=email)
        if response.exists():  # 如果用户名已经存在
            contex['err_msg'] = "该邮箱已被注册"
            return render(request, "register.html", contex)
        response=email_record.objects.filter(addr=email)
        if not response.exists() or \
                response[0].verify_code != verify_code or \
                    int(time.time())-response[0].time>300:
            contex['err_msg']="验证码无效或已过期"
            return render(request,"register.html",contex)
        data = users()#写入数据库
        data.username = username
        data.password = password
        data.nickname = nickname
        data.email=email
        data.register_date = datetime.datetime.now()
        data.save()  # 写入
        request.session['tip'] = "注册成功，请您登陆"
        return HttpResponseRedirect("/login")

    if request.method == "GET":
        contex = dict()
        if 'tip' in request.session:
            contex['tip'] = request.session['tip']
            del request.session['tip']
        return render(request, "register.html", contex)


def login(request):
    if request.method == "POST":
        username, password = LoginData(request).get_data()
        if username == None:
            return HttpResponse("数据不合法")
        contex = dict()
        contex['err_msg'] = "用户名或密码错误"
        contex['username'] = username
        response = users.objects.filter(Q(username=username)|Q(email=username))
        if not response.exists():  # 用户不存在
            return render(request, "login.html", contex)
        if response[0].password != password:  # 密码错误
            return render(request, "login.html", contex)
        session = request.session
        user_id=response[0].id
        session['user_id'] = user_id  # 设置session
        return HttpResponseRedirect("/index")
    if request.method == "GET":
        contex = dict()
        if 'tip' in request.session:
            contex['tip'] = request.session['tip']
            del request.session['tip']
        return render(request, "login.html", contex)


def logout(request):
    request.session.flush()
    request.session['tip'] = "您已成功登出，请重新登陆"
    return HttpResponseRedirect('/login')



class Encrypt:  # 用于加密密码
    def __init__(self):
        conf = settings.conf
        self.salt = conf.get("login", "salt")

    def encrypt(self, str):
        str = self.salt + str + self.salt
        str = str.encode(encoding="utf-8")
        str = hashlib.md5(str).hexdigest()
        return str


class GetPostData:
    def __init__(self, request):
        self.receive_data = request.POST
        self.username = self.receive_data.get('username')
        self.password = self.receive_data.get('password')
        if self.post_lawful():
            self.password = Encrypt().encrypt(self.password)
        else:
            self.username = None  # 如果数据不合法，就将self.username置为None，方便后面的判断

    # 防止绕过前端验证，提交非法内容
    def post_lawful(self):
        if self.username is None or self.password is None \
                or len(self.username) < 3 or len(self.username)  > 20 \
                or len(self.password) <8 or len(self.password) > 20:
            return False
        else:
            return True


class RegisterData(GetPostData):
    def __init__(self, request):
        super().__init__(request)
        self.nickname = self.receive_data.get('nickname')
        self.email=self.receive_data.get('email')
        self.verify_code=self.receive_data.get('verify_code')
    def get_data(self):
        if self.username is not None and self.lawful():
            return self.username, self.password, self.nickname,self.email,self.verify_code
        else:
            return None, None, None,None,None

    def lawful(self):
        if self.nickname is None or len(self.nickname) < 2 or len(self.nickname)>10:
            return False
        else:
            return True


class LoginData(GetPostData):
    def __init__(self, request):
        super().__init__(request)

    def get_data(self):
        return self.username, self.password

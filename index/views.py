import os
from django.shortcuts import render
from index.models import emotion
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from EmotionAnalyse import settings  # 为了节省代码没有重写读取ini文件的代码而是直接引入settings
import hashlib


# 因为不习惯使用自带的用户认证机制，所以自己重写了login，logout，register
def register(request):
    if request.method == "POST":
        username, password, nickname = RegisterData(request).get_data()
        if username == None:
            return HttpResponse("数据不合法")
        contex = dict()
        contex['nickname'] = nickname
        contex['username'] = username
        response = emotion.objects.filter(nickname=nickname)
        if response.exists():  # 如果昵称已经存在
            contex['err_msg'] = "昵称已存在"
            return render(request, "register.html", contex)
        response = emotion.objects.filter(username=username)
        if response.exists():  # 如果用户名已经存在
            contex['err_msg'] = "用户名已存在"
            return render(request, "register.html", contex)
        data = emotion()
        data.username = username
        data.password = password
        data.nickname = nickname
        data.register_date = datetime.datetime.now()
        data.save()  # 注册成功，写入数据库
        request.session['tip'] = "注册成功，请您登陆"
        return HttpResponseRedirect("/index/login")

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
        response = emotion.objects.filter(username=username)
        if not response.exists():  # 用户不存在
            return render(request, "login.html", contex)
        response = list(response)
        if response[0].password != password:  # 密码错误
            return render(request, "login.html", contex)
        session = request.session
        session['username'] = username  # 设置session
        session['nickname'] = response[0].nickname
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
    return HttpResponseRedirect('/index/login')


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
    if 'username' in session:
        contex = dict()
        contex['username'] = session['username']
        contex['nickname'] = session['nickname']
        return render(request, "index.html", contex)
    else:
        session['tip'] = "您还未登陆，请先登陆"
        return HttpResponseRedirect("/index/login")


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
                or len(self.username) < 5 or len(self.password) < 8 \
                or len(self.password) > 15 or len(self.password) > 12:
            return False
        else:
            return True


class RegisterData(GetPostData):
    def __init__(self, request):
        super().__init__(request)
        self.nickname = self.receive_data.get('nickname')

    def get_data(self):
        if self.username is not None and self.lawful():
            return self.username, self.password, self.nickname
        else:
            return None, None, None

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

from django.http import HttpResponse,JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from api.models import email_record,token_record
import random
import time
from django.core.mail import send_mail
from django.shortcuts import render
import hashlib
from django.db.models import Q
@csrf_exempt
def api(request):
    if request.method=="POST":
        data=request.POST
        err_code,emotion=Api.deal()
        result=dict()
        result['err_code']=err_code
        if err_code==0:
            result['emotion']=emotion
        return JsonResponse(result)

class Api:
    max_length=1024
    def __init__(self,data):
        self.data=data
    def check(self):
        data=self.data
        token=data.get('token')
        token_find=token_record.objects.filter(Q(token1=token)|Q(token2=token))
        if not token_find.exists:
            return 1001

    def deal(self):
        err_code=self.check()
        if err_code!=0:
            return err_code,None

@csrf_exempt
def token(self,request):
    if request.method=="GET":
        data=request.GET
        err_code,token=Token(data).token()
        result=dict()
        result['err_code']=err_code
        result['token']=token
        result=json.dumps(result)
        return HttpResponse(result,content_type='application/json,charset=utf-8')
    def check(self,data):
        pass
class Token:
    def __init__(self,data):
        self.data=data
    def check(self):
        data=self.data
        id=data.get('id')
        self.id=id
        key=data.get('key')
        if id is None or key is None:
            return 1001
        return 0
    def token(self):
        err_code=self.check()
        if err_code!=0:
            return err_code,None
        else:
            str=self.id+time.strftime("%H ")
            str = str.encode(encoding="utf-8")
            str = hashlib.md5(str).hexdigest()
            return



@csrf_exempt
def email(request):#发送验证码的视图函数
    if request.method=='POST':
        addr=request.POST.get('addr')
        why=request.POST.get('why')#why表示需要验证码的原因 注册，找回密码等
        sender=VerifyCode(why,addr)
        send_result=sender.send()
        result=dict()
        if send_result==1:
            result['status']="success"
        else:
            result['status']="fail"
        return JsonResponse(result)
    else:
        return render(request,"test.html")


class VerifyCode:
    def __init__(self,why,to_addr):
        self.to_addr=to_addr
        if why=="Register":
            self.title="注册"
        elif why=="FindPassword":
            self.title="找回密码"
        self.verify_code=self.generate()
    def generate(self):
        code=''
        for i in range(6):
            code=code+str(random.randint(0,9))
        return code
    def send(self):
        find=email_record.objects.filter(addr=self.to_addr)
        if find.exists():
            find=find[0]
            find.verify_code=self.verify_code
            find.time=int(time.time())
            find.save()
        else:
            data = email_record()
            data.addr=self.to_addr
            data.verify_code=self.verify_code
            data.time=int(time.time())
            data.save()
        message="您的验证码为：{}，验证码5分钟有效。".format(self.verify_code)
        return send_mail(subject='验证码', message=message,from_email=None,recipient_list=[self.to_addr], fail_silently=False)

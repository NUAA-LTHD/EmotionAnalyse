from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from api.models import email_record
import random
import time
from django.core.mail import send_mail
from django.shortcuts import render
@csrf_exempt
def api(request):
    if request.method=="POST":
        error_code=0
        text_max_length=512
        result = dict()
        while True:
            try:
                data=json.loads(request.body.decode(encoding='utf-8'))
            except Exception as err:
                error_code=1001
                print(err)
                break
            if ('token' not in data) or ('text' not in data) or (len(data)!=2):
                error_code=1002
                break
            token=data['token']
            text=data['text']
            if len(text)>text_max_length:
                error_code=2001
            result['text']=text
            break
        result['error_code']=error_code
        result=json.dumps(result)
        return HttpResponse(result,content_type='application/json,charset=utf-8')
    else:
        result={'error_code':1003}
        result=json.dumps(result)
        return HttpResponse(result,content_type='application/json,charset=utf-8')
@csrf_exempt
def token(request):
    if request.method=="GET":
        result=dict()
        error_code=0
        while True:
            id=request.GET.get('id')
            key=request.GET.get('key')
            if id==None or key==None:
                error_code = 1001
                break
            token="123"
            result['token']=token
            break
        result['error_code']=error_code
        result=json.dumps(result)
        return HttpResponse(result,content_type='application/json,charset=utf-8')


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
@csrf_exempt
def email(request):#发送验证码的视图函数
    if request.method=='POST':
        addr=request.POST.get('addr')
        why=request.POST.get('why')#why表示需要验证码的原因 注册，找回密码等
        sender=VerifyCode(why,addr)
        response=sender.send()
        if response==1:
            return HttpResponse("success")
        else:
            return HttpResponse("fail")
    else:
        return render(request,"test.html")
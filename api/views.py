from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
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
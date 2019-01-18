from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from app1.serializers import UserSerializer, GroupSerializer
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import exceptions
import json
from app1 import models
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class MyBaseView(object):

    def dispatch(self, request, *args, **kwargs):
        print('before')
        ret = super(StudentsView, self).dispatch(request, *args, **kwargs)
        print('after')
        return ret

class StudentsView(MyBaseView, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('GET')
    def post(self, request, *args, **kwargs):
        return HttpResponse('POST')
    def put(self, request, *args, **kwargs):
        return HttpResponse('PUT')
    def delete(self, request, *args, **kwargs):
        return HttpResponse('DELETE')

@method_decorator(csrf_exempt,name='dispatch')
class Teacher(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(StudentsView, self).dispatch(request, *args, **kwargs)

class MyAuthentication(object):
    def authenticate(self,request):
        token = request._request.GET.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return ('alex', None)
    def authenticate_header(self,val):
        pass

class DogView(APIView):
    authentication_classes = [MyAuthentication,]
    def get(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'msg': 'xxx'
        }
        return HttpResponse(json.dumps(ret),status=201)
    def post(self, request, *args, **kwargs):
        return HttpResponse('POST')
    def put(self, request, *args, **kwargs):
        return HttpResponse('PUT')
    def delete(self, request, *args, **kwargs):
        return HttpResponse('DELETE')


def md5(user):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    def post(self,request,*args,**kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('pwd')
            obj = models.UserInfo.objects.filter(username=user,password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            token = md5(user)
            models.UserToken.objects.update_or_create(user=obj,defaults={'token':token})
            ret['token'] = token
        except Exception:
            ret['code'] = 1002
            ret['msg'] = '请求异常'


        return JsonResponse(ret)
class Authentication(APIView):
    def authenticate(self,request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return (token_obj.user, token_obj)
    def authenticate_header(self,val):
        pass

class OrderView(APIView):
    authentication_classes = [Authentication,]
    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        ret = {'code': 1000, 'msg': None, 'data': 'sadsfdsf'}
        return JsonResponse(ret)

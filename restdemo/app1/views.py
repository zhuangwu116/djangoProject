from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from app1.serializers import UserSerializer, GroupSerializer
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import exceptions
import json
import time
from app1 import models
from rest_framework.throttling import BaseThrottle
from rest_framework.versioning import BaseVersioning
from rest_framework.parsers import JSONParser
from rest_framework import serializers


class RolesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


# class UserInfoSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#     type = serializers.ChoiceField(source='user_type')
#     type_name = serializers.ChoiceField(source='get_user_type_display')
#     gp = serializers.CharField(source="group.title")
#     rls = serializers.SerializerMethodField()
#     def get_rls(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({'id': item.id, 'title': item.title})
#         return ret
# class UserInfoSerializer(serializers.ModelSerializer):
#     rls = serializers.SerializerMethodField()
#     type_name = serializers.ChoiceField(source='get_user_type_display')
#     def get_rls(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({'id': item.id, 'title': item.title})
#         return ret
#
#     class Meta:
#         models = models.UserInfo
#         field = ['id', 'username', 'password', 'type_name', 'user_type', 'rls']


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.UserInfo
        field = '__all__'
        depth = 1


class RolesView(APIView):
    def get(self, request, *args, **kwargs):
        # roles = models.Role.objects.all()
        # ser = RolesSerializer(instance=roles, many=True)
        # ret = json.dumps(ser.data, ensure_ascii=False)

        roles = models.Role.objects.all().first()
        ser = RolesSerializer(instance=roles, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = RolesSerializer(instance=users, many=True)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


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


@method_decorator(csrf_exempt, name='dispatch')
class Teacher(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(StudentsView, self).dispatch(request, *args, **kwargs)


class MyAuthentication(object):
    def authenticate(self, request):
        token = request._request.GET.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return ('alex', None)

    def authenticate_header(self, val):
        pass


class SVIPPermission(object):
    message = '必须是SVIP才能访问'

    def has_permission(self, request, view):
        return True


class DogView(APIView):
    authentication_classes = [MyAuthentication, ]

    def get(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'msg': 'xxx'
        }
        return HttpResponse(json.dumps(ret), status=201)

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
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('pwd')
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            token = md5(user)
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token
        except Exception:
            ret['code'] = 1002
            ret['msg'] = '请求异常'

        return JsonResponse(ret)


class Authentication(APIView):
    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return (token_obj.user, token_obj)

    def authenticate_header(self, val):
        pass


VISIT_RECORD = {}


class VisitThrottle(BaseThrottle):
    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # 1.获取用户IP
        remote_addr = self.get_ident(request)
        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime, ]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history
        while history and history[-1] < ctime - 60:
            history.pop()
        if len(history) < 3:
            history.insert(0, ctime)
            return True

    # return True #return False 表示访问频率太高，被限制
    def wait(self):
        # 还需要等多少秒才能访问
        ctime = time.time()
        ctime = 60 - (ctime - self.history[-1])

        return ctime


class OrderView(APIView):
    authentication_classes = [Authentication, ]
    permission_classes = [SVIPPermission, ]
    throttle_classes = [VisitThrottle, ]

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        ret = {'code': 1000, 'msg': None, 'data': 'sadsfdsf'}
        return JsonResponse(ret)


class ParamVersion(object):
    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get('version')
        return version


class UsersView(APIView):
    versioning_class = ParamVersion

    def get(self, request, *args, **kwargs):
        print(request.version)
        return HttpResponse('用户列表')


class ParserView(APIView):
    parser_classes = [JSONParser, ]

    def post(self, request, *args, **kwargs):
        # 允许用户发送JSON格式数据
        print(request.data)

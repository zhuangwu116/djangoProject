from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from app1.serializers import UserSerializer, GroupSerializer
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator

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
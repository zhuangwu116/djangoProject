from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from app1.serializers import UserSerializer, GroupSerializer
from django.views import View

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


class StudentsView(View):
    def dispatch(self, request, *args, **kwargs):
        ret = super(StudentsView, self).dispatch(request, *args, **kwargs)
        return ret
    def get(self, request, *args, **kwargs):
        self.dispatch(request, *args, **kwargs)
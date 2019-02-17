from django.shortcuts import render


from rest_framework import viewsets,mixins

from .models import UserFav
from .serializers import UserFavSerializer
# Create your views here.
class UserFaviewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
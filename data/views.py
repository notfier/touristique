from django.shortcuts import render

from rest_framework import generics, authentication, permissions

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentList(generics.ListAPIView):

    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentInfo(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    """
    Update/Get/Add a tourist card.
    GET: get a tourist card info by its tourist card pk.
    PUT: update a tourist card info with itself data.
    POST: create a new tourist card providing all necessary data.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = DepartmentSerializer

    def get_object(self):
        if self.request.method == 'GET':
            department_pk = self.request.query_params.get('department_pk')
        elif self.request.method == 'PUT':
            department_pk = self.request.data.get('department_pk')
        return Department.objects.get(pk=department_pk)

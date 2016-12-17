from rest_framework import serializers

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentField(serializers.Field):

    def to_representation(self, obj):
        return DepartmentSerializer(obj).data

    def to_internal_value(self, dep_pk):
        return Department.objects.get(pk=dep_pk)

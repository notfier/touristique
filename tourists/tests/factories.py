# -*- coding: utf-8 -*-
import factory

from data.tests.factories import DepartmentFactory

from ..models import Tourist, TouristCard


class TouristFactory(factory.DjangoModelFactory):

    class Meta:
        model = Tourist

    first_name = 'Dave'
    last_name = 'Greel'
    email = 'greel@musicians.com'


class TouristCardFactory(factory.DjangoModelFactory):

    class Meta:
        model = TouristCard

    tourist = factory.SubFactory(TouristFactory)
    current_department = factory.SubFactory(DepartmentFactory)

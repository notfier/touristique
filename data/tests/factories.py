# -*- coding: utf-8 -*-
import factory

from ..models import Department


class DepartmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = Department

    name = factory.Sequence(lambda n: 'Dep#{0}'.format(n))
    address = factory.Sequence(lambda n: 'Carrer de Sant Fructuos {0}'.format(n))
    zip_code = factory.Sequence(lambda n: '{0}{1}'.format(n, n+1))
    phone = '12345'

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Department(models.Model):
    """
    Model to realize Department.
    """

    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)

    class Meta:
        verbose_name = _('department')
        verbose_name_plural = _('departments')

    def __unicode__(self):
        return '{0}'.format(self.name)

from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from data.models import Department


class Tourist(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(blank=True, max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('tourist')
        verbose_name_plural = _('tourists')

    def get_full_name(self):
        return ' '.join(
            filter(None, (self.first_name, self.middle_name, self.last_name))
        )

    def __unicode__(self):
        return self.get_full_name()


class TouristCard(models.Model):
    """
    Unique ID card model for tourists.
    """

    card_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tourist = models.OneToOneField(Tourist, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    current_department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('tourist_card')
        verbose_name_plural = _('tourist_cards')

    def __unicode__(self):
        return '{0}\'s card'.format(self.tourist)

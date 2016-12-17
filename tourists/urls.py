from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'tourist_info/(?P<tourist_pk>\d+)/$', view=views.TouristInfo.as_view(), name='tourists-info'),
    url(r'tourist_card_info/$', view=views.TouristCardInfo.as_view(), name='tourists-card-info'),
]

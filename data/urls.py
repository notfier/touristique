from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'departments/$', view=views.DepartmentList.as_view(), name='data-get-departments'),
    url(r'get_department/$', view=views.DepartmentInfo.as_view(), name='data-get-department'),
]

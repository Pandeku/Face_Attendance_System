from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^exam_login/$', views.exam_login, name='exam_login'),
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r'^all_students/$', views.all_students, name='all_students')
]
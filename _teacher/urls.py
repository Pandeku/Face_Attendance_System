from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^teacher_login/$', views.teacher_login, name='teacher_login'),
    url(r'^add_student/$', views.add_student, name='add_student'),
    url(r'^delete_student/$', views.delete_student, name='delete_student'),
    url(r'^delete_face/$', views.delete_face, name='delete_face'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
]
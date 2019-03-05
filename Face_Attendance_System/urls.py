# -*- coding:UTF-8 -*-
"""Face_Attendance_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import include, url
from _index import views
urlpatterns = [
    url(r'^_exam/', include('_exam.urls')),
    url(r'^_search/', include('_search.urls')),
    url(r'^_teacher/', include('_teacher.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^logout/', views.logout),
    url(r'^clean/', views.logout),
    # url(r'^update/', views.update),
    # url(r'^test/', views.test),
]
handler400 = views.bad_request
handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.page_error

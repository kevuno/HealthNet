"""healthnet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from log.views import stats_alt


urlpatterns = [
    url(r'^', include('home.urls')),

    url(r'^admin/stats?', stats_alt),

    url(r'^admin/?', admin.site.urls),

    url(r'^appointments/?', include('appointment.urls')),

    url(r'^employee/?', include('employee.urls')),

    url(r'^userprofile/?', include('userprofile.urls')),

    url(r'^medrecord/?', include('medrecord.urls')),

    url(r'^messages/?', include('messaging.urls'))

    # url(r'^goodbye', include('home.urls')),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

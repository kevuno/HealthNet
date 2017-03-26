from django.conf.urls import url

from . import views

app_name = 'messaging'
urlpatterns = [

    #/messages
    url(r'^$', views.index, name='index'),

    #/messages/inbox
    url(r'^inbox/?$', views.inbox, name='inbox'),

    url(r'^(?P<message_id>[0-9]+)/?$', views.message_detail, name='detail'),

    #/messages/compose
    url(r'^compose/?$', views.ComposeMessage.as_view(), name='compose')

]
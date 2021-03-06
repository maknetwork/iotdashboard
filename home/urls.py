from django.urls import path
from . import views
from django.conf.urls import url
from .views import connect

app_name='home'
urlpatterns = [
# post views
path('', views.homepage, name='homepage'),
path('connect', connect.as_view(), name='connect'),
path('disconnect', views.disconnect, name='disconnect'),

    url(r'^savedata/$', views.saveflybox, name='saveflybox'),
                url(r'^startautomation/$', views.startautomation, name='start_automation'),
url(r'^disconnect_client', views.disconnectclient, name='disconnectclient'),


]

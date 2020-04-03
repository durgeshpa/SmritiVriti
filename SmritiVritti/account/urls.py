from django.urls import path,include
from django.conf.urls import url
from . import views
app_name='account'
urlpatterns = [

path('',views.registration,name='registration'),
url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	views.activate, name='activate'),
url(r'^conformotp',views.conform_otp ,name = 'conform_otp')
   
]

from django.urls import path
from .views import *

app_name = 'tutorial'

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('gettoken/', gettoken, name='gettoken'),
    path('mail/', mail, name='mail'),
    path('events/', events, name='events'),
    path('contacts/', contacts, name='contacts')
]

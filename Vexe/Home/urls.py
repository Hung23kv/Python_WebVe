from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    path('Trip/',views.HTrip,name='tripHome'),
    path('Detail/<int:id>',views.Detail,name="detail"),
    path('Login/',views.Login,name = 'login'),
    path('InfoUser/',views.info_user,name='info_user'),
]
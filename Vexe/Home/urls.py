from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('Trip/',views.Trip,name='trip'),
    path('Detail/',views.Detail,name="detail"),
    path('Chose_seat/',views.Seat,name = 'seat')
]
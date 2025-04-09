from django.urls import path
from . import views
urlpatterns = [
    path('',views.homeAd,name='homeAdmin'),
    path('bus',views.GetBus,name='bus'),
    path('bus/<int:id>',views.DetailBus,name = 'detailBus'),
    path('delete/<int:id>',views.deleteBus,name = 'deleteBus'),
    path('bus/creat_bus',views.insertBus,name = 'insertBus'),
]
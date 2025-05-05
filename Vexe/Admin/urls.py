from django.urls import path
from . import views



urlpatterns = [
    path('',views.homeAd,name='homeAdmin'),
    path('bus',views.GetBus,name='bus'),
    path('bus/<int:id>',views.DetailBus,name = 'detailBus'),
    path('delete/<int:id>',views.deleteBus,name = 'deleteBus'),
    path('bus/creat_bus',views.insertBus,name = 'insertBus'),
    path('route',views.GetRoute,name = 'Route'),
    path('route/creat_route',views.insertRoute,name = 'insertRoute'),
    path('trip/<int:id>',views.editTrip,name = 'modifyRoute'),
    
    path('pickup/delete/<int:id>', views.deletePickup, name='delete_pickup'),
    path('dropoff/delete/<int:id>', views.deleteDropoff, name='delete_dropoff'),
    path('trip',views.GetTrip,name = 'trip'),
    path('trip/create_trip',views.insertTrip,name = 'insertTrip'),
    path('trip/add/<int:id>',views.insertPickDrop,name = 'insertPickDrop'),
    path('Ticker',views.GetTicker,name = 'ticker'),
]
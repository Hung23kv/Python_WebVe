from django.shortcuts import render
from Admin.models import Trip,Route
# Create your views here.
def home(request):
    data = Trip.objects.raw('''
        SELECT t.id, t.route_id, t.ticket_price, r.id AS route_id, r.place, r.destination
        FROM trip t
        JOIN route r ON t.route_id = r.id
        LIMIT 5
    ''')
    return render(request,'Home.html',{"ListTrip": data})
def HTrip(request):
    return render(request,'InfoTrip.html')
def Detail(request):
    return render(request,'Detail.html')
def Seat(request):
    return render(request,'ChoseSeat.html')
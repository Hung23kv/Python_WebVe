from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'Home.html')
def Trip(request):
    return render(request,'InfoTrip.html')
def Detail(request):
    return render(request,'Detail.html')
def Seat(request):
    return render(request,'ChoseSeat.html')
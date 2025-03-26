from django.shortcuts import render

# Create your views here.
def homeAd(request):
    return render(request,'baseAdmin.html')
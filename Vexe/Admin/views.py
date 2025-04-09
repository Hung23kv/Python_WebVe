from django.shortcuts import render,redirect
from .models import Bus
from django.contrib import messages

# Create your views here.
def homeAd(request):
    return render(request,'HomeAdmin.html')
def GetBus(request):
    data = Bus.objects.all()    
    return render(request,'ManageBus.html',{"listBus" : data})
def insertBus(request):
    if request.method == "POST":
        name = request.POST.get('txtName')
        type = request.POST.get('txtType')
        seat_count = request.POST.get('txtGhe')
        license_plate = request.POST.get('txtlicense_plate')
        image = request.FILES.get('txtimages') 

        bus = Bus.objects.create(name = name,type = type,seat_count = seat_count,license_plate = license_plate,image = image)
        bus.save()
        messages.success(request,"Thêm xe thành công !")
        return redirect('/admin/bus')
    return render(request,'insertBus.html')
def DetailBus(request,id):
    data = Bus.objects.get(id=id)
    if request.method == "POST":
        name = request.POST.get('txtName')
        type = request.POST.get('txtType')
        seat_count = request.POST.get('txtGhe')
        license_plate = request.POST.get('txtlicense_plate')
        image = request.FILES.get('txtimages') 

        bus = Bus.objects.get(id=id)
        bus.name = name
        bus.type = type
        bus.seat_count = seat_count
        bus.license_plate = license_plate
        if image:
            bus.image = image
        bus.save()
        messages.success(request,"Sua thông tin xe thành công !")
        return redirect('/admin/bus')
    
    return render(request,'EditBus.html',{"Detail" : data})
def deleteBus(request,id):
    data = Bus.objects.get(id=id)
    data.delete()
    messages.success(request,"Xóa xe thành công !")
    return redirect('/admin/bus')
  
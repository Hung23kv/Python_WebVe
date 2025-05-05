from django.shortcuts import render,redirect
from .models import Bus,Route,Trip,Pickup,Dropoff,Ticket
from django.contrib import messages
from .Role import admin_required

# Create your views here.
@admin_required
def homeAd(request):
    return render(request,'HomeAdmin.html')
@admin_required
def GetBus(request):
    data = Bus.objects.all()    
    return render(request,'ManageBus.html',{"listBus" : data})
@admin_required
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
@admin_required
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
@admin_required
def deleteBus(request,id):
    data = Bus.objects.get(id=id)
    data.delete()
    messages.success(request,"Xóa xe thành công !")
    return redirect('/admin/bus')
@admin_required
def GetRoute(request):
    data = Route.objects.all()
    return render(request,'ManageRoute.html',{"listRoute" : data})
@admin_required
def insertRoute (request):
    if request.method == "POST":
        place = request.POST.get('tinh')
        destination = request.POST.get('tinh2')
        distance = request.POST.get('txtKhoangC')
        duration = request.POST.get('txtTime')
        route = Route.objects.create(place = place,destination = destination,distance = distance,duration = duration)
        route.save()
        messages.success(request,"Thêm tuyến thành công !")
        return redirect('/admin/route')
    return render(request,'insertRoute.html')
@admin_required
def GetTrip(request):
    data = Trip.objects.all()
    
    trip = []
    for  i in data:
        route = Route.objects.get(id=i.route_id)
        trip_format = {
            'id' : i.id,
            'bus' : i.bus,
            'route' : route.place + " - " + route.destination,
            'ticket_price' : i.ticket_price,
            'available_seats' : i.available_seats,
            'status' : i.status,
            'departure_date' : i.departure_date.strftime('%d/%m/%Y')
        }
        trip.append(trip_format)
    return render(request,'ManageTrip.html',{"listTrip" : trip})
@admin_required
def insertTrip(request):
    data = Bus.objects.exclude(trip__isnull=False)
    data2 = Route.objects.all()
    if request.method == "POST":
        bus = request.POST.get('cboBus')
        route = request.POST.get('cboRoute')
        ticket_price = request.POST.get('txtPrice')
        selected_bus = Bus.objects.get(id=bus)
        available_seats = selected_bus.seat_count
        status = request.POST.get('cboStatus')
        departure_date = request.POST.get('txtDate')
        trip = Trip.objects.create(bus_id = bus,route_id = route,ticket_price = ticket_price,available_seats = available_seats,status = status,departure_date = departure_date)
        trip.save()
        return redirect('/admin/trip/add/' + str(trip.id))   
    return render(request,'insertTrip.html',{"listBus" : data,"listRoute" : data2})
@admin_required
def insertPickDrop(request,id):
    if request.method == "POST":
        numPick = request.POST.get('numPickupPoints')
        numDrop = request.POST.get('numDropoffPoints')
        
        # Sửa range bắt đầu từ 1 để khớp với template
        for i in range(1, int(numPick) + 1):
            pickup_location = request.POST.get(f'pickupLocation{i}')
            pickup_time = request.POST.get(f'pickupTime{i}')
            pickup = Pickup.objects.create(
                trip_id=id,
                location=pickup_location,
                time=pickup_time
            )
            pickup.save()
            
        for i in range(1, int(numDrop) + 1):
            drop_location = request.POST.get(f'dropoffLocation{i}')
            drop_time = request.POST.get(f'dropoffTime{i}')
            drop = Dropoff.objects.create(
                trip_id=id,
                location=drop_location,
                time=drop_time
            )
            drop.save()
            
        return render(request, 'InsertDrop_Pick.html', {
                'id': id,
                'show_success': True,
                'message': 'Thêm chuyến đi thành công !!!'
            })
    return render(request,'InsertDrop_Pick.html',{"id" : id})
@admin_required
def GetTicker(request):
    trips = Trip.objects.select_related('route').all()
    trip_list = []
    for trip in trips:
        trip_format = {
            'id': trip.id,
            'route': f"{trip.route.place} - {trip.route.destination}",
            'departure_date': trip.departure_date.strftime('%d/%m/%Y')
        }
        trip_list.append(trip_format)

    context = {
        "listGotrip": trip_list,
        "selected_trip_id": None,
        "listTicket": None 
    }
        
    if request.method == "POST":
        trip_id = request.POST.get('cboTrip')
        if trip_id:  
            tickets = Ticket.objects.filter(trip_id=trip_id).select_related('user')
            context.update({
                "selected_trip_id": int(trip_id),
                "listTicket": tickets
            })

    return render(request, 'ManageTicker.html', context)
@admin_required
def editTrip(request, id):
    trip = Trip.objects.select_related('route', 'bus').get(id=id)
    buses = Bus.objects.all()
    routes = Route.objects.all()
    pickups = Pickup.objects.filter(trip_id=id)
    dropoffs = Dropoff.objects.filter(trip_id=id)

    if request.method == "POST":
        try:
            
            bus_id = request.POST.get('cboBus')
            route_id = request.POST.get('cboRoute')
            ticket_price = request.POST.get('txtPrice')
            available_seats = request.POST.get('txtSeats')
            status = request.POST.get('cboStatus')
            departure_date = request.POST.get('txtDate')

            
            trip.bus_id = bus_id
            trip.route_id = route_id
            trip.ticket_price = ticket_price
            trip.available_seats = available_seats
            trip.status = status
            trip.departure_date = departure_date
            trip.save()

            
            if 'time-input[]' in request.POST:
                pickup_ids = request.POST.getlist('id_don[]')
                pickup_times = request.POST.getlist('time-input[]')
                pickup_locations = request.POST.getlist('location-input[]')
                
                for i in range(len(pickup_ids)):
                    Pickup.objects.filter(id=pickup_ids[i]).update(
                        time=pickup_times[i],
                        location=pickup_locations[i]
                    )

            
            if 'time-tra[]' in request.POST:
                dropoff_ids = request.POST.getlist('id_tra[]')
                dropoff_times = request.POST.getlist('time-tra[]')
                dropoff_locations = request.POST.getlist('location-tra[]')
                
                for i in range(len(dropoff_ids)):
                    Dropoff.objects.filter(id=dropoff_ids[i]).update(
                        time=dropoff_times[i],
                        location=dropoff_locations[i]
                    )

            
            if 'newpickupTime[]' in request.POST:
                new_pickup_times = request.POST.getlist('newpickupTime[]')
                new_pickup_locations = request.POST.getlist('newpickupLocation[]')
                
                for i in range(len(new_pickup_times)):
                    if new_pickup_times[i] and new_pickup_locations[i]:
                        Pickup.objects.create(
                            trip_id=id,
                            time=new_pickup_times[i],
                            location=new_pickup_locations[i]
                        )

            
            if 'newDropoffTime[]' in request.POST:
                new_dropoff_times = request.POST.getlist('newDropoffTime[]')
                new_dropoff_locations = request.POST.getlist('newDropoffLocation[]')
                
                for i in range(len(new_dropoff_times)):
                    if new_dropoff_times[i] and new_dropoff_locations[i]:
                        Dropoff.objects.create(
                            trip_id=id,
                            time=new_dropoff_times[i],
                            location=new_dropoff_locations[i]
                        )

            messages.success(request, "Cập nhật chuyến đi thành công!")
            return redirect('/admin/trip')

        except Exception as e:
            messages.error(request, f"Lỗi khi cập nhật: {str(e)}")
            return redirect(f'/admin/trip/edit/{id}')

    context = {
        'trip': trip,
        'buses': buses,
        'routes': routes,
        'pickups': pickups,
        'dropoffs': dropoffs
    }
    
    return render(request, 'EditTrip.html', context)
@admin_required
def deletePickup(request, id):
    pickup = Pickup.objects.get(id=id)
    trip_id = pickup.trip_id
    pickup.delete()
    messages.success(request, "Xóa điểm đón thành công!")
    return redirect(f'/admin/trip/edit/{trip_id}')
@admin_required
def deleteDropoff(request, id):
    dropoff = Dropoff.objects.get(id=id)
    trip_id = dropoff.trip_id
    dropoff.delete()
    messages.success(request, "Xóa điểm trả thành công!")
    return redirect(f'/admin/trip/edit/{trip_id}')
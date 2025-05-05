from django.shortcuts import render,redirect
from Admin.models import Trip,Users,Pickup,Dropoff,Ticket
from django.contrib import messages
from django.db.models import Q
import datetime
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
    data = Trip.objects.all()
    for t in data:
        t.departure_date = t.departure_date.strftime("%d/%m/%Y")
    return render(request,'InfoTrip.html',{"list": data})
def Detail(request,id):
    data = Trip.objects.get(id=id)
    data1 = Pickup.objects.filter(trip=id)
    data2 = Dropoff.objects.filter(trip=id)
    if data:
        data.departure_date = data.departure_date.strftime("")
    
    if request.method == 'POST':
        quantity = request.POST.get('seatQuantity')
        price = request.POST.get('price')
        user_id = request.session.get('user_name')
        user_book = Users.objects.get(name=user_id)
        trip_id = Trip.objects.get(id=id)
        seat_number = quantity + " ghế"
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'Chưa thanh toán'
        tikcet = Ticket.objects.create(user=user_book,trip=trip_id,quantity=quantity,total_price=price,seat_numbers=seat_number,booking_time=date,status=status)
        tikcet.save()
        return redirect('home')
    return render(request,'Detail.html',{"trip": data,"pickup": data1,"dropoff": data2})
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('passw')
        user = Users.objects.filter(Q(email=username) | Q(phone=username) , password=password).first()
        if user:
            request.session['user_name'] = user.name
            admin = user.role
            admin = admin.strip()
            request.session['role'] = admin
            if admin == 'admin':
                return redirect('/admin/')
            return redirect('home')
        else:
            messages.error(request, 'Nhập sai thông tin tài khoản!')
    return render(request,'Login.html')

def info_user(request):
    if not request.session.get('user_name'):
        return redirect('login')
        
    user = Users.objects.get(name=request.session.get('user_name'))
    tickets = Ticket.objects.filter(user=user).select_related(
        'trip', 'trip__route', 'trip__bus'
    ).order_by('-booking_time')
    
    return render(request, 'InfoUser.html', {
        'user': user,
        'tickets': tickets
    })
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
import time,datetime
import calendar
from .models import Room,Genre,User,Order



def get_time_seet(flg_holiday):
    if (flg_holiday):
        return ['10:00~11:00', '11:15~12:15', '13:15~14:15', '14:30~15:30', '15:45~16:45']
    else:
        return ['15:00~16:00', '16:15~17:15', '17:30~18:30']

def	index(request):
	return render(request,'umbrella_system/index.html')

def	date(request, dates):
    gdate = int(dates)
    year = gdate//10000
    day = gdate%100
    month = (gdate%10000-day)//100

    day_of_week = datetime.date(year, month, day).weekday()
    flg_holiday = False
    if (day_of_week == 5 or day_of_week == 6):
        flg_holiday = True
    
    if 'user_name' in request.session:
        session = dict({'user_name':request.session['user_name']})
    else:
            return HttpResponseRedirect(reverse('umbrella_system:login'))

    calendar.setfirstweekday(calendar.SUNDAY)
    dt = datetime.datetime.fromtimestamp(time.mktime((year, month+1, 1, 0, 0, 0, 0, 0, 0)))
    next_date = dict({'year':dt.year,'month':dt.month,})
    dt = datetime.datetime.fromtimestamp(time.mktime((year, month-1, 1, 0, 0, 0, 0, 0, 0)))
    last_date = dict({'year':dt.year,'month':dt.month,})
    cal = dict({'year':year,'month':month,'day':day,'days':calendar.monthcalendar(year, month),})
    dt = datetime.datetime(year, month, day)
    rooms = Room.objects.all()

    if (flg_holiday):
        time_set = 6;
        time_seet = ['10:00~11:00', '11:15~12:15', '13:15~14:15', '14:30~15:30', '15:45~16:45']
    else:
        time_set = 4;
        time_seet = ['15:00~16:00', '16:15~17:15', '17:30~18:30']
    roomset=[]
    for rooma in rooms:
        orders = Order.objects.filter(room=rooma,order_day=dt)
        wari=[]

        for i in range(1, time_set):
            wari.append(dict({'time':i,'time_zone':time_seet[i-1],}))
        for order in orders:
            wari[order.time_zone_id-1] = dict({'time':order.time_zone_id,'time_zone':time_seet[order.time_zone_id-1],'user':order.user.name,'genre':order.genre.name})
        wari = sorted(wari, key=lambda wari: wari['time'])
        roomset.append(dict({'room_name':rooma.name,'seats':rooma.seats,'wari':wari}))

    contexts = dict({'cal':cal,'next_date':next_date,'last_date':last_date,'rooms':Room.objects.all(),'roomset':roomset,'flg_holiday':flg_holiday})
    contexts.update(session)

    return HttpResponse(render(request,'umbrella_system/date.html',contexts))

def room(request):
    contexts = dict({'messages': Room.objects.all(),})
    rooms = Room.objects.all()
    for rooma in rooms:
        orders = rooma.order_set.exclude()
        wari = dict({})
        for order in orders:
            wari.update({'time':order.time_zone_id,'user':order.user.name})
        contexts[rooma] = wari
    return HttpResponse(render(request, 'umbrella_system/room.html', contexts))

def login(request):
    contexts = dict({'error_messages': ''})
    if 'user_name' in request.session:
        session = dict({'user_name':request.session['user_name']})
        dt = datetime.date.today()
        if(dt.month//10==0):
            date = str(dt.year)+'0'+str(dt.month)+'01'
        else:
            date = str(dt.year)+''+str(dt.month)+'01'
        return HttpResponseRedirect(reverse('umbrella_system:date', args=(date,)))
    return HttpResponse(render(request, 'umbrella_system/login.html', contexts))

def login_go(request):
    selected_user=User.objects.get(name=request.POST['user_name'])
    if selected_user.password != request.POST['password']:
        contexts = dict({'error_messages': 'NO ID OR PASSWORD'})
        return HttpResponse(render(request, 'umbrella_system/login.html', contexts))
    else:
        request.session['user_name'] = selected_user.name
        dt = datetime.date.today()
        if(dt.month//10==0):
            date = str(dt.year)+'0'+str(dt.month)+'01'
        else:
            date = str(dt.year)+''+str(dt.month)+'01'
        return HttpResponseRedirect(reverse('umbrella_system:date', args=(date,)))


def logout(request):
    if 'user_name' in request.session:
        del request.session['user_name']
    contexts = dict({'error_messages': ''})

    return HttpResponseRedirect(reverse('umbrella_system:login',))

def yoyaku(request,dates,room,time):
    if 'user_name' in request.session:
        session = dict({'user_name':request.session['user_name']})
    else:
        return HttpResponseRedirect(reverse('umbrella_system:login'))
    year = int(dates)//10000
    day = int(dates)%100
    month = (int(dates)%10000-day)//100
    dt = datetime.datetime(year, month, day)
    try:
        if (Order.objects.filter(room=Room.objects.get(name=room), time_zone_id=time, order_day=dt).count() > 0):
            raise Http404
        else:
            selected_genre = Genre.objects.all()
            contexts = dict({'genres': selected_genre, 'date': dates, 'time': time, 'room': room})
            return HttpResponse(render(request, 'umbrella_system/yoyaku.html', contexts))
    except (KeyError, Room.DoesNotExist):
        raise Http404

def yoyaku_touroku(request):
    if 'user_name' in request.session:
        session = dict({'user_name':request.session['user_name']})
        uname = request.session['user_name']
    else:
            return HttpResponseRedirect(reverse('umbrella_system:login'))
    try:

        selected_genre = Genre.objects.get(name=request.POST['genres'])
        selected_user = User.objects.get(name=uname)
        selected_room = Room.objects.get(name=request.POST['room'])
        order = Order()
    except (KeyError, Room.DoesNotExist,User.DoesNotExist,Genre.DoesNotExist):
        contexts = dict({'error_message': 'NO DATE'})
        return HttpResponse(render(request, 'umbrella_system/index.html', contexts))
    else:
        year = int(request.POST['date'])//10000
        day = int(request.POST['date'])%100
        month = (int(request.POST['date'])%10000-day)//100
        dt = datetime.datetime(year, month, day)
        order.room = selected_room
        order.genre = selected_genre
        order.user = selected_user
        order.time_zone_id = request.POST['time']
        order.order_day = dt
        order.charge_lv = request.POST['charge_lv']
        order.save()
        return HttpResponseRedirect(reverse('umbrella_system:date', args=(request.POST['date'],)))
def yoyaku_del(request,dates,room,time):
    if 'user_name' in request.session:
        session = dict({'user_name':request.session['user_name']})
    else:
        return HttpResponseRedirect(reverse('umbrella_system:login'))
    year = int(dates)//10000
    day = int(dates)%100
    month = (int(dates)%10000-day)//100
    dt = datetime.datetime(year, month, day)
    try:
        if (Order.objects.filter(room=Room.objects.get(name=room), time_zone_id=time, order_day=dt,user=User.objects.get(name=request.session['user_name'])).count() == 1):
            selected_order = Order.objects.get(room=Room.objects.get(name=room), time_zone_id=time, order_day=dt,user=User.objects.get(name=request.session['user_name']))
            contexts = dict({'room': selected_order.room.name, 'date': dates, 'time': selected_order.time_zone_id, 'genre': selected_order.genre,'charge':selected_order.charge_lv})
            return HttpResponse(render(request, 'umbrella_system/yoyakudel.html', contexts))
        else:
            raise Http404
    except (KeyError, Room.DoesNotExist,User.DoesNotExist):
        raise Http404
def yoyaku_del_go(request):
    if 'user_name' in request.session:
        session = dict({'user_name':request.session['user_name']})
        uname = request.session['user_name']
    else:
            return HttpResponseRedirect(reverse('umbrella_system:login'))
    try:
        selected_user = User.objects.get(name=uname)
        selected_room = Room.objects.get(name=request.POST['room'])
    except (KeyError, Room.DoesNotExist,User.DoesNotExist,Genre.DoesNotExist):
        raise Http404
    else:
        year = int(request.POST['date'])//10000
        day = int(request.POST['date'])%100
        month = (int(request.POST['date'])%10000-day)//100
        dt = datetime.datetime(year, month, day)
        selected_order = Order.objects.get(room=selected_room,user=selected_user,time_zone_id=request.POST['time'], order_day=dt).delete()
        return HttpResponseRedirect(reverse('umbrella_system:date', args=(request.POST['date'],)))

def	zikanwari(request, dates):
    gdate = int(dates)
    year = gdate//100
    day = 1
    month = gdate%100

    if 'user_name' in request.session:
        session = dict({'user_name':request.session['user_name']})
    else:
            return HttpResponseRedirect(reverse('umbrella_system:login'))

    dt = datetime.datetime.fromtimestamp(time.mktime((year, month+1, -1, 0, 0, 0, 0, 0, 0)))
    cal = dict({'year':year,'month':month,})


    dt = datetime.datetime(year, month, day)
    rooms = Room.objects.all()
    days = []
    for day_set in range(1, datetime.datetime.fromtimestamp(time.mktime((year, month+1, -1, 0, 0, 0, 0, 0, 0))).day+1):
        if (datetime.datetime(year, month, day_set).weekday() == 5 or datetime.datetime(year, month, day_set).weekday() == 6):
            time_set = 6;
            time_seet =['10:00~11:00','11:15~12:15','13:15~14:15','14:30~15:30','15:45~16:45']
        else:
            time_set = 4;
            time_seet =['15:00~16:00','16:15~17:15','17:30~18:30']
        roomset = []
        for rooma in rooms:
            orders = Order.objects.filter(room=rooma, order_day=datetime.datetime(year, month, day_set))
            wari = []

            for i in range(1, time_set):
                wari.append(dict({'time': i}))
            for order in orders:
                wari[order.time_zone_id - 1] = dict(
                    {'time': order.time_zone_id, 'user': order.user.name, 'genre': order.genre.name})
            wari = sorted(wari, key=lambda wari: wari['time'])
            roomset.append(dict({'room_name': rooma.name, 'seats': rooma.seats, 'wari': wari}))
        days.append(dict({'day':day_set,'time_seet':time_seet,'weekday':datetime.datetime(year, month, day_set).weekday(),'rooms':roomset,}))
    contexts = dict({'cal':cal,'days':days,})
    contexts.update(session)
    return HttpResponse(render(request,'umbrella_system/zikanwari.html',contexts))

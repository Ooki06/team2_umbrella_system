from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
import time,datetime
import calendar
from .models import Room,Genre,User,Order




def	index(request):
	return render(request,'umbrella_system/index.html')

def	date(request, dates):
    gdate = int(dates)
    year = gdate//10000
    day = gdate%100
    month = (gdate%10000-day)//100

    if 'user_name' in request.session:
        session = dict({'user_name':request.session['user_name']})
    else:
            return HttpResponseRedirect(reverse('umbrella_system:login'))

    calendar.setfirstweekday(calendar.SUNDAY)
    dt = datetime.datetime.fromtimestamp(time.mktime((year, month+1, 1, 0, 0, 0, 0, 0, 0)))
    next_date = dict({'year':dt.year,'month':dt.month,})
    dt = datetime.datetime.fromtimestamp(time.mktime((year, month-1, 1, 0, 0, 0, 0, 0, 0)))
    last_date = dict({'year':dt.year,'month':dt.month,})
    cal = dict({'year':year,'month':month,'days':calendar.monthcalendar(year, month),})
    dt = datetime.datetime(year, month, day)
    rooms = Room.objects.all()
    i = 0
    roomset={}
    for rooma in rooms:
        orders = Order.objects.filter(room=rooma,order_day=dt)
        wari={}
        for order in orders:
            times = dict({'time':order.time_zone_id,'user':order.user.name})
            wari.update({order.time_zone_id:times})
        room = dict({'name':rooma.name,'wari':wari})
        roomset.update({rooma.name:room})
        i += 1

    contexts = dict({'cal':cal,'next_date':next_date,'last_date':last_date,'rooms':Room.objects.all(),'roomset':roomset,'i':i})

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
        return HttpResponseRedirect(reverse('umbrella_system:date', args=('20160601',)))
    return HttpResponse(render(request, 'umbrella_system/login.html', contexts))

def login_go(request):
    selected_user=User.objects.get(name=request.POST['user_name'])
    if selected_user.password != request.POST['password']:
        contexts = dict({'error_messages': 'NO ID OR PASSWORD'})
        return HttpResponse(render(request, 'umbrella_system/login.html', contexts))
    else:
        request.session['user_name'] = selected_user.name
        return HttpResponseRedirect(reverse('umbrella_system:date', args=('20160601',)))


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
    selected_genre = Genre.objects.all()
    contexts = dict({'genres': selected_genre,'date':dates,'time':time,'room':room})
    return HttpResponse(render(request, 'umbrella_system/yoyaku.html', contexts))

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
    except (KeyError, User.DoesNotExist):
        contexts = dict({'error_message': 'NO DATE'})
        return HttpResponse(render(request, 'umbrella_system/yoyaku.html', contexts))
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
        return HttpResponseRedirect(reverse('umbrella_system:date', args=('20160601',)))

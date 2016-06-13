from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
import time,datetime
import calendar

def	index(request):
	return render(request,'umbrella_system/index.html')

def	date(request, dates):
    gdate = int(dates)
    year = gdate//100
    month = gdate%100

    calendar.setfirstweekday(calendar.SUNDAY)
    dt = datetime.datetime(year,month,1)
    dt = datetime.datetime.fromtimestamp(time.mktime((year, month+1, 1, 0, 0, 0, 0, 0, 0)))
    next_date = dict({'year':dt.year,'month':dt.month,})
    dt = datetime.datetime.fromtimestamp(time.mktime((year, month-1, 1, 0, 0, 0, 0, 0, 0)))
    last_date = dict({'year':dt.year,'month':dt.month,})

    cal = dict({'year':year,'month':month,'days':calendar.monthcalendar(year, month),})
    contexts = dict({'cal':cal,'next_date':next_date,'last_date':last_date,})

    return HttpResponse(render(request,'umbrella_system/date.html',contexts))
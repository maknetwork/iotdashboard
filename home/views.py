from django.shortcuts import render
from django.views.generic.edit import CreateView  # new
from .models import Clients, Sensors
from django.views.generic import TemplateView
from django.db.models import Avg

from django.http import HttpResponse, HttpResponseRedirect
from bs4 import BeautifulSoup
import requests
import pytz
from django.http import HttpResponse, JsonResponse
# Create your views here.
import datetime
import os
from datetime import datetime as dt
from datetime import timedelta
from chartjs.views.lines import BaseLineChartView
def homepage(request):

    date = []
    temperature = []
    humidity = []
    luminosity = []
    clients= Clients.objects.all()
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    use=Sensors.objects.filter(date__range=(today_min, today_max))
    sensordata=Sensors.objects.filter().order_by('-id')[0]

    avg= use.aggregate(Avg('temperature'))
    print(avg)
    d = dt.today() - timedelta(days=1)


    queryset = Sensors.objects.all()
    for city in queryset:
        user= datetime.datetime.strptime(str(city.date.date()), '%Y-%m-%d').strftime('%A')
        date.append(str(city.date.date()))
        temperature.append(city.temperature)
        humidity.append(city.humidity)
        luminosity.append(city.luminosuty)

    state="on"



    return render(request, 'home/home.html',{'date': date,'clients':clients,
        'temperature': temperature,'humidity':humidity,'luminosity':luminosity, 'status':state,'sensordata':sensordata})

class connect(CreateView):  # new

    model = Clients
    template_name = 'home/connect.html'
    fields = '__all__'

def saveflybox(request):

    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        try:
            title = request.POST.get('name')
            ipaddress = request.POST.get('ipaddress')
            URL = "http://%s" %ipaddress
            r = requests.get(URL)

            soup = BeautifulSoup(r.content, 'html5lib')
            inputs=soup.find("input", {"id": "input-id"})
            print(inputs['value'])
            if inputs['value']== "hello":
                user = Clients.objects.create(title=title, ipaddress=ipaddress)
                user.save()
                return JsonResponse({'success':True})
            else:
                return HttpResponse('Device either offline or DoesNotExist')
        except Exception as e:
            return JsonResponse({'error':str(e)})

    else:

        return HttpResponseRedirect('')



def startautomation(request):

    id = request.GET.get('dept_id')
    buttonpressed = request.GET.get('user_name')

    cronnamer= Clients.objects.get(pk=id)

    if buttonpressed=="off" :
        cmd= 'curl '+ cronnamer.ipaddress +'/5/off'
        os.system(cmd)

    elif buttonpressed=="on":
        cmd= 'curl '+ cronnamer.ipaddress +'/5/on'
        os.system(cmd)





    print(buttonpressed)
    return HttpResponseRedirect('/')

from django.shortcuts import render
from django.views.generic.edit import CreateView  # new
from .models import Clients, Sensors
from django.views.generic import TemplateView
from django.db.models import Avg
from django.views.decorators.cache import never_cache

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

@never_cache
def homepage(request):

    date = []
    temperature = []
    humidity = []
    luminosity = []
    clients= Clients.objects.all()
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    state="on"
    sensordata= Sensors.objects.latest('id')

    for client in clients:

        try:

            URL = "http://"+ client.ipaddress
            r = requests.get(URL)
            soup = BeautifulSoup(r.content, 'html5lib')
            inputs3=soup.find("input", {"id": "status"})
            state= (inputs3['value'])
        except:
            print("not found")
    return render(request, 'home/home.html',{'date': date,'clients':clients,'sensordata':sensordata, "status":state})

class connect(CreateView):  # new

    model = Clients
    template_name = 'home/connect.html'
    fields = '__all__'

def disconnect(request):
    posts = Clients.objects.all()
    return render(request, 'home/disconnect.html', {'posts': posts})

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


def disconnectclient(request):

    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        try:
            pk = request.POST.get('clientid')
            post = Clients.objects.get(pk=pk)
            post.delete()
            return JsonResponse({'success':True})
        except:
            return JsonResponse({'error':"false"})


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

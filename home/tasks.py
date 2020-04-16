from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import Clients, Sensors
from bs4 import BeautifulSoup
import requests
import pytz
logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_save_latest_flickr_image",
    ignore_result=True
)

def task_save_latest_flickr_image():
    clients= Clients.objects.filter()
    print(clients)

    for client in clients:
        try:
            URL = "http://"+ client.ipaddress
            r = requests.get(URL)
            soup = BeautifulSoup(r.content, 'html5lib')
            inputs=soup.find("input", {"id": "humidity"})
            inputs2=soup.find("input", {"id": "temperature"})
            inputs3=soup.find("input", {"id": "luminosity"})

            humi= (inputs['value'])
            temp= (inputs2['value'])
            lumi=(inputs3['value'])
            user = Sensors.objects.create(client=client, temperature=int(float(temp)), humidity=int(float(humi)), luminosuty=int(lumi))
            user.save()
            client.connected= True
            client.save()

            logger.info("Saved image from Flickr")
        except:
            client.connected= False
            client.save()
            print("client not found")

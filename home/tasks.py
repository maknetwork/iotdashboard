from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import Clients, Sensors
from bs4 import BeautifulSoup
import requests
import pytz
logger = get_task_logger(__name__)

lumi=2000
@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_save_latest_flickr_image",
    ignore_result=True
)

def task_save_latest_flickr_image():
    client= Clients.objects.get(pk=2)

    URL = "http://192.168.0.109"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')
    inputs=soup.find("input", {"id": "humidity"})
    humi= (inputs['value'])
    inputs2=soup.find("input", {"id": "temperature"})
    humi= (inputs['value'])
    temp= (inputs2['value'])
    user = Sensors.objects.create(client=client, temperature=int(float(temp)), humidity=int(float(humi)), luminosuty=lumi)
    user.save()



    logger.info("Saved image from Flickr")

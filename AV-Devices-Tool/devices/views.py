from django.shortcuts import render
from devices.models import Device


# Create your views here.
def index(request):
    
    # Query all devices
    devices = Device.objects.all().select_related('room__building__campus', 'category')
    
    context = {
        'devices': devices
    }
    return render(request, 'devices/index.html', context)
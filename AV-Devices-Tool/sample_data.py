import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'av_tool.settings')
django.setup()  

from django.contrib.auth.models import User
from devices.models import Campus, Building, Room, Category, Device

def create_sample_data():
    # Create a superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        print('Superuser created successfully.')
        
    # Create campuses
    campus1 = Campus.objects.create(campus_name='Main Campus')
    campus2 = Campus.objects.create(campus_name='Second Campus')
    
    # Create buildings
    building1 = Building.objects.create(building_name='Building A', campus=campus1)
    building2 = Building.objects.create(building_name='Building B', campus=campus2)
    
    # Create rooms
    room1 = Room.objects.create(room_number='101', building=building1)
    room2 = Room.objects.create(room_number='102', building=building2)
    
    # Create categories
    category1 = Category.objects.create(category_name='Control Processor', description='Extron control processors')
    category2 = Category.objects.create(category_name='Display', description='Monitors and TVs')

    # Create Devices
    Device.objects.create(
        model_name='IPCP Pro 550',
        ip_address='192.168.1.100',
        mac_address='00-05-A6-0E-9E-5E',
        hostname='device1',
        location='Main Campus',
        contact='John Doe',
        vendor='Extron',
        serial_number='A18WRHV',
        device_link='http://example.com/device/1',
        room=room1,
        category=category1,
        status=True
    )
    Device.objects.create(
        model_name='DTP 84 switcher',
        ip_address='192.168.1.102',
        mac_address='00-05-A6-0E-9E-5F',
        hostname='device2',
        location='Second Campus',
        contact='Jane Doe',
        vendor='Samsung',
        serial_number='B29XSGW',
        device_link='http://example.com/device/2',
        room=room2,
        category=category2,
        status=True
    )
    
    print('Sample data created successfully.')
    
if __name__ == '__main__':
    create_sample_data()
from django.contrib.auth.models import User
from devices.models import Campus, Building, Room, Category

def create_sample_data():
    # Create a superuser
    if not User.objects.filter(username='admin').exists():
        USer.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        
    # Create a sample data
    campus1 = Campus.objects.create(campus_name='Main Campus')
    campus2 = Campus.objects.create(campus_name='Second Campus')
    
    building1 = Building.objects.create(building_name='Building A', campus=campus1)
    building2 = Building.objects.create(building_name='Building B', campus=campus2)
    
    room1 = Room.objects.create(room_number='101', building=building1)
    room2 = Room.objects.create(room_number='102', building=building2)
    
    category1 = Category.objects.create(category_name='Control Processor', description='Extron control processors')
    category2 = Category.objects.create(category_name='Display', description='Monitors and TVs')

    Device.objects.create(
        model_name='IPCP Pro 550',
        ip_address='192.168.1.100',
        mac_address='00-05-A6-0E-9E-5E',
        hostname='device1',
        serial_number='A18WRHV',
        firmware_version='3.16.0001-b002',
        device_link='http://example.com/device/1',
        room=room1,
        category=category1
    )
    Device.objects.create(
        model_name='Samsung QLED',
        ip_address='192.168.1.101',
        mac_address='00-05-A6-0E-9E-5F',
        hostname='device2',
        serial_number='B29XSGW',
        firmware_version='2.0.1',
        device_link='http://example.com/device/2',
        room=room2,
        category=category2
    )
    
    if __name__ == '__main__':
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'av_tool.settings')
        import django
        django.setup()
        create_sample_data()
        print('Sample data created successfully.')
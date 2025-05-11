from django.db import models

# Create your models here.
class Campus(models.Model):
    campus_id = models.AutoField(primary_key=True)
    campus_name = models.CharField(max_length=250, null=False)
    
    def __str__(self):
        return self.campus_name
    
class Building(models.Model):
    building_id = models.AutoField(primary_key=True)
    building_name = models.CharField(max_length=250, null=False)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='buildings')
    
    def __str__(self):
        return self.building_name
    
class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=50, null=False)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    
    def __str__(self):
        return f'{self.room_number} (Building: {self.building.building_name}, Campus: {self.building.campus.campus_name})'
    
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    
    def __str__(self):
        return self.category_name
    
class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=100, null=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    hostname = models.CharField(max_length=250,blank=True, null=True)
    location = models.CharField(max_length=250, default='Not Specified', null=True)
    contact = models.CharField(max_length=250, default='Not Specified', null=True)
    vendor = models.CharField(max_length=250, default='Not Specified', null=True)
    serial_number = models.CharField(max_length=250, null=True)
    device_link = models.URLField(blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='devices')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=False, editable=False)
    
    def __str__(self):
        return f'{self.model_name} ({self.ip_address})'
    
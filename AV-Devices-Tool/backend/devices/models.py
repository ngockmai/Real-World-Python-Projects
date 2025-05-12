from django.db import models
from django.utils import timezone

# Create your models here.
class Campus(models.Model):
    campus_id = models.AutoField(primary_key=True)
    campus_name = models.CharField(max_length=250, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Campuses"
        ordering = ['campus_name']
        db_table = 'campus'
    
    def __str__(self):
        return self.campus_name
    
class Building(models.Model):
    building_id = models.AutoField(primary_key=True)
    building_name = models.CharField(max_length=250, null=False)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='buildings')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['campus', 'building_name']
        db_table = 'building'
    
    def __str__(self):
        return f'{self.building_name} ({self.campus.campus_name})'
    
class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=50, null=False)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['building', 'room_number']
        unique_together = ['building', 'room_number']
        db_table = 'room'
    
    def __str__(self):
        return f'{self.room_number} (Building: {self.building.building_name}, Campus: {self.building.campus.campus_name})'
    
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['category_name']
        db_table = 'category'
    
    def __str__(self):
        return self.category_name
    
class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=100, null=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    hostname = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, default='Not Specified', null=True)
    contact = models.CharField(max_length=250, default='Not Specified', null=True)
    vendor = models.CharField(max_length=250, default='Not Specified', null=True)
    serial_number = models.CharField(max_length=250, null=True)
    device_link = models.URLField(blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='devices')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    firmware_version = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['model_name', 'ip_address']
        db_table = 'device'
    
    def __str__(self):
        return f'{self.model_name} ({self.ip_address or "No IP"})'
    
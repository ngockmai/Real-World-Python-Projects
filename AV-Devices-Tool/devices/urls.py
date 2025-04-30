from django.urls import path
from . import views

app_name = "devices"

urlpatterns = [
    path("", views.index, name="index"),
    path("devices", views.get_devices, name="get_devices"),
    path("devices/location/<int:location_id>/", views.get_devices_by_location, name="get_devices_by_location"),
    path("devices/room/<int:room_id>/", views.get_devices_by_room, name="get_devices_by_room"),
    # path("devices/<int:device_id>/", views.device_detail, name="device_detail"),
]
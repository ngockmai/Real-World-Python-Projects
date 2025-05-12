from django.urls import path
from .views import DeviceListView, DeviceByRoomView, DeviceByLocationView, DeviceDetailView, LocationListView, LocationDetailView, TreeView

api_urlpatterns = [
    # Devices
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('devices/room/<int:room_id>/', DeviceByRoomView.as_view(), name='device_by_room'),
    path('devices/location/<int:location_id>/', DeviceByLocationView.as_view(), name='device_by_location'),
    path('devices/<int:device_id>/', DeviceDetailView.as_view(), name='device_detail'),
    
    # Locations
    path('locations/', LocationListView.as_view(), name='location_list'),
    path('locations/<int:location_id>/', LocationDetailView.as_view(), name='location_detail'),
    
    # Treeview
    path('locations/treeview/', TreeView.as_view(), name='treeview'),
]
from django.urls import path
from .views import DeviceListView, DeviceDetailView, ControllerListView, ControllerDetailView, RoomListView, RoomDetailView

api_urlpatterns = [
    # Devices
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('devices/<int:device_id>/', DeviceDetailView.as_view(), name='device_detail'),
    path('controllers/', ControllerListView.as_view(), name='controller_list'),
    path('controllers/<int:controller_id>/', ControllerDetailView.as_view(), name='controller_detail'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/<int:room_id>/', RoomDetailView.as_view(), name='room_detail'),
    
    # path('devices/room/<int:room_id>/', DeviceByRoomView.as_view(), name='device_by_room'),
    # path('devices/location/<int:location_id>/', DeviceByLocationView.as_view(), name='device_by_location'),
    
    
    # # Locations
    # path('locations/', LocationListView.as_view(), name='location_list'),
    # path('locations/<int:location_id>/', LocationDetailView.as_view(), name='location_detail'),
    
    # # Treeview
    # path('locations/treeview/', TreeView.as_view(), name='treeview'),
]
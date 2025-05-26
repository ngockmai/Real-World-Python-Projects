from django.urls import path
from .views import DeviceListView, DeviceDetailView, ControllerListView, ControllerDetailView, RoomListView, RoomDetailView, LocationListView, LocationDetailView, ModelListView, ManufacturerListView, ModelDetailView, ManufacturerDetailView, TreeView

api_urlpatterns = [
    # Devices
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('device/<int:device_id>/', DeviceDetailView.as_view(), name='device_detail'),
    path('controllers/', ControllerListView.as_view(), name='controller_list'),
    path('controller/<int:controller_id>/', ControllerDetailView.as_view(), name='controller_detail'),
    
    # Models
    path('models/', ModelListView.as_view(), name='model_list'),
    path('model/<int:model_id>/', ModelDetailView.as_view(), name='model_detail'),
    
    # Manufacturers
    path('manufacturers/', ManufacturerListView.as_view(), name='manufacturer_list'),
    path('manufacturer/<int:manufacturer_id>/', ManufacturerDetailView.as_view(), name='manufacturer_detail'),
    # Rooms
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('room/<int:room_id>/', RoomDetailView.as_view(), name='room_detail'),
    
    # path('devices/room/<int:room_id>/', DeviceByRoomView.as_view(), name='device_by_room'),
    # path('devices/location/<int:location_id>/', DeviceByLocationView.as_view(), name='device_by_location'),
    
    # Locations
    path('locations/', LocationListView.as_view(), name='location_list'),
    path('location/<int:location_id>/', LocationDetailView.as_view(), name='location_detail'),
    
    # Treeview
    path('locations/treeview/', TreeView.as_view(), name='treeview'),
]
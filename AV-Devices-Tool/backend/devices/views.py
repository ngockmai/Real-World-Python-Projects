from rest_framework.views import APIView
from rest_framework import status
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
# from devices.utils import authenticate_session, parse_device_name, process_devices
# from devices.models import Device
import requests
from django.conf import settings
import logging
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime

logger = logging.getLogger('devices')

def authenticate_session():
    auth_url = "https://gve3.ad.umanitoba.ca:443/GVE/api/auth"
    auth_payload = {
        "UserName" : settings.API_USERNAME,
        "Password" : settings.API_PASSWORD,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    session = requests.Session()
    
    try:
        response = session.post(auth_url, json=auth_payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return session, None
    except (requests.RequestException, ValueError) as e:
        logger.error(f"Authentication failed: {str(e)}")
        return None, f"Authentication failed: {str(e)}"

# MongoDB connection
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
devices_collection = db['devices']
controllers_collection = db['controllers']
rooms_collection = db['rooms']
locations_collection = db['locations']
models_collection = db['models']
manufacturers_collection = db['manufacturers']
treeview_collection = db['locations_treeview']

###  Devices
# Fetch and update devices
def update_devices():
    session, error = authenticate_session()
    if error:
        logger.error(f"Scheduled update failed - Authentication error: {error}")
        return

    try:
        devices_url = f"{settings.GVE_API_URL}/devices"
        devices_response = session.get(devices_url, headers={"Accept": "application/json"}, timeout=10)
        devices_response.raise_for_status()
        devices_data = devices_response.json()
        devices = devices_data.get("Devices", [])
        
        # Track unique ModelId and ManufacturerId to avoid duplicate API calls
        fetched_model_ids = set()
        fetched_manufacturer_ids = set()

        for device in devices:
            live_status = device.get("LiveStatus", {})
            device_doc = {
                "DeviceId": device.get("DeviceId"),
                "RoomId": device.get("RoomId"),
                "ControllerId": device.get("ControllerId"),
                "ModelId": device.get("ModelId"),
                "DeviceName": device.get("DeviceName"),
                "DeviceType": device.get("DeviceType"),
                "Status": device.get("Status"),
                "ControllerPortType": device.get("ControllerPortType"),
                "ControllerPortNumber": device.get("ControllerPortNumber"),
                "PowerOnPowerConsumption": device.get("PowerOnPowerConsumption"),
                "PowerOffPowerConsumption": device.get("PowerOffPowerConsumption"),
                "LampCost": device.get("LampCost"),
                "LiveStatus": {
                    "Connection": live_status.get("Connection"),
                    "Power": live_status.get("Power"),
                    "DeviceStatus": live_status.get("DeviceStatus"),
                    "LampHours": live_status.get("LampHours"),
                    "MaxLampHours": live_status.get("MaxLampHours"),
                    "OperationHours": live_status.get("OperationHours"),
                    "FilterHours": live_status.get("FilterHours"),
                    "MaxFilterHours": live_status.get("MaxFilterHours"),
                },
                "ControllerCommandGuid": device.get("ControllerCommandGuid"),
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            devices_collection.update_one(
                {"DeviceId": device.get("DeviceId")},
                {"$set": device_doc},
                upsert=True
            )
            
            # Fetch and update model data
            model_id = device.get("ModelId")
            if model_id and model_id not in fetched_model_ids:
                model_url = f"{settings.GVE_API_URL}/devices/model/{model_id}"
                model_response = session.get(model_url, headers={"Accept": "application/json"}, timeout=10)
                model_response.raise_for_status()
                model_data = model_response.json().get("Model", {})
                model_doc = {
                    "ModelId": model_data.get("ModelId"),
                    "ModelName": model_data.get("ModelName"),
                    "ManufacturerId": model_data.get("ManufacturerId"),
                    "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                models_collection.update_one(
                    {"ModelId": model_doc["ModelId"]},
                    {"$set": model_doc},
                    upsert=True
                )
                fetched_model_ids.add(model_id)
                
                # Fetch manufacturer data only if not already fetched
                manufacturer_id = model_data.get("ManufacturerId")
                if manufacturer_id and manufacturer_id not in fetched_manufacturer_ids:
                    manufacturer_url = f"{settings.GVE_API_URL}/devices/manufacturer/{manufacturer_id}"
                    manufacturer_response = session.get(manufacturer_url, headers={"Accept": "application/json"}, timeout=10)
                    manufacturer_response.raise_for_status()
                    manufacturer_data = manufacturer_response.json().get("Manufacturer", {})
                    manufacturer_doc = {
                        "ManufacturerId": manufacturer_data.get("ManufacturerId"),
                        "ManufacturerName": manufacturer_data.get("ManufacturerName"),
                        "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    manufacturers_collection.update_one(
                        {"ManufacturerId": manufacturer_doc["ManufacturerId"]},
                        {"$set": manufacturer_doc},
                        upsert=True
                    )
                    fetched_manufacturer_ids.add(manufacturer_id)

        logger.info(f"Devices updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CDT")
    except requests.RequestException as e:
        logger.error(f"Scheduled update failed - Error fetching devices: {str(e)}")
        
# Function to fetch and update controllers
def update_controllers():
    session, error = authenticate_session()
    if error:
        logger.error(f"Scheduled update failed - Authentication error: {error}")
        return

    try:
        controllers_url = f"{settings.GVE_API_URL}/controllers"
        controllers_response = session.get(controllers_url, headers={"Accept": "application/json"}, timeout=10)
        controllers_response.raise_for_status()
        controllers_data = controllers_response.json()
        controllers = controllers_data.get("Controllers", [])

        for controller in controllers:
            network_settings = controller.get("NetworkSettings", {})
            controller_doc = {
                "ControllerId": controller.get("ControllerId"),
                "ControllerName": controller.get("ControllerName"),
                "Status": controller.get("Status"),
                "RoomId": controller.get("RoomId"),
                "IsOnline": controller.get("IsOnline"),
                "NetworkSettings": {
                    "HostName": network_settings.get("HostName"),
                    "GatewayIPAddress": network_settings.get("GatewayIPAddress"),
                    "SubnetMask": network_settings.get("SubnetMask"),
                    "IsDhcpEnabled": network_settings.get("IsDhcpEnabled")
                },
                "MacAddress": controller.get("MacAddress"),
                "ControllerType": controller.get("ControllerType"),
                "ModelName": controller.get("ModelName"),
                "PartNumber": controller.get("PartNumber"),
                "FirmwareVersion": controller.get("FirmwareVersion"),
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            controllers_collection.update_one(
                {"ControllerId": controller.get("ControllerId")},
                {"$set": controller_doc},
                upsert=True
            )
        logger.info(f"Controllers updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CDT")
    except requests.RequestException as e:
        logger.error(f"Scheduled update failed - Error fetching controllers: {str(e)}")
        

# Function to fetch and update rooms
def update_rooms():
    session, error = authenticate_session()
    if error:
        logger.error(f"Scheduled update failed - Authentication error: {error}")
        return

    try:
        rooms_url = f"{settings.GVE_API_URL}/rooms"
        rooms_response = session.get(rooms_url, headers={"Accept": "application/json"}, timeout=10)
        rooms_response.raise_for_status()
        rooms_data = rooms_response.json()
        rooms = rooms_data.get("Rooms", [])

        for room in rooms:
            room_doc = {
                "RoomId": room.get("RoomId"),
                "RoomName": room.get("RoomName"),
                "LocationId": room.get("LocationId"),
                "Category": room.get("Category"),
                "Status": room.get("Status"),
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            rooms_collection.update_one(
                {"RoomId": room.get("RoomId")},
                {"$set": room_doc},
                upsert=True
            )
        logger.info(f"Rooms updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CDT")
    except requests.RequestException as e:
        logger.error(f"Scheduled update failed - Error fetching rooms: {str(e)}")

# Fetch and update locations
def update_locations():
    session, error = authenticate_session()
    if error:
        logger.error(f"Scheduled update failed - Authentication error: {error}")
        return

    try:
        locations_url = f"{settings.GVE_API_URL}/locations"
        locations_response = session.get(locations_url, headers={"Accept": "application/json"}, timeout=10)
        locations_response.raise_for_status()
        locations_data = locations_response.json()
        locations = locations_data.get("Locations", [])

        for location in locations:
            location_doc = {
                "LocationId": location.get("LocationId"),
                "LocationName": location.get("LocationName"),
                "ParentLocationId": location.get("ParentLocationId"),
                "Status": location.get("Status"),
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            locations_collection.update_one(
                {"LocationId": location.get("LocationId")},
                {"$set": location_doc},
                upsert=True
            )
        logger.info(f"Locations updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CDT")
    except requests.RequestException as e:
        logger.error(f"Scheduled update failed - Error fetching locations: {str(e)}")

# Fetch and update the location tree view from API
def update_treeview():
    session, error = authenticate_session()
    if error:
        logger.error(f"Scheduled update failed - Authentication error: {error}")
        return
    
    try:
        treeview_url = f"{settings.GVE_API_URL}/locations/treeview"
        treeview_response = session.get(treeview_url, headers={"Accept": "application/json"}, timeout=10)
        treeview_response.raise_for_status()
        treeview_data = treeview_response.json()
        locations = treeview_data.get("Locations", [])
        
        # Build a map of LocationId to Location data for quick lookup
        location_map = {}
        for item in locations:
            location = item.get("Location")
            if location:
                loc_id = location.get("LocationId")
                location_map[loc_id] = {
                    "id" : loc_id,
                    "name" : location.get("LocationName"),
                    "status" : location.get("Status"),
                    "children" : [
                       {
                        "id" : room.get("RoomId"),
                        "name" : room.get("RoomName"),
                        "status" : room.get("Status"),
                        "category" : room.get("Category"),
                        "children" : []
                       } for room in item.get("Rooms", [])
                    ]
                }
            
            treeview_doc = {
                "LocationId": item.get("Location").get("LocationId"),
                "LocationName": item.get("Location").get("LocationName"),
                "ParentLocationId": item.get("Location").get("ParentLocationId"),
                "Status": item.get("Location").get("Status"),
                "Rooms": item.get("Rooms"),
                "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            treeview_collection.update_one(
                {"LocationId": treeview_doc["LocationId"]},
                {"$set": treeview_doc},
                upsert=True
            )
        logger.info(f"Treeview updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CDT")
        
    except requests.RequestException as e:
        logger.error(f"Scheduled update failed - Error fetching treeview: {str(e)}")
        
# Serve devices from MongoDB
class DeviceListView(APIView):
    def get(self, request):
        force_update = request.GET.get('force_update', 'false').lower() == 'true'

        if force_update:
            update_devices()
            stored_devices = list(devices_collection.find({}, {"_id": 0}))
            total = len(stored_devices)
            return JsonResponse({
                'devices': stored_devices,
                'total': total,
                'last_updated': stored_devices[0]["last_updated"] if stored_devices else None,
                'message': 'Devices updated manually'
            }, status=status.HTTP_200_OK)

        try:
            # Retrieve all devices from MongoDB
            stored_devices = list(devices_collection.find({}, {"_id": 0}))
            total = len(stored_devices)
            
            return JsonResponse({
                'devices': stored_devices,
                'total': total
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching devices from MongoDB: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Get single device with ID
class DeviceDetailView(APIView):
    def get(self, request, device_id):
        try:
            device = devices_collection.find_one({"DeviceId": device_id}, {"_id": 0})
            if not device:
                return JsonResponse({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'device': device}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching device details: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

# Get models from MongoDB
class ModelListView(APIView):
    def get(self, request):
        try:
            stored_models = list(models_collection.find({}, {"_id": 0}))
            total = len(stored_models)
            if stored_models:
                return JsonResponse({
                    'models': stored_models,
                    'total': total,
                    'last_updated': stored_models[0]["last_updated"] if stored_models else None
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.error(f"Error fetching models from MongoDB: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Get single model with ID
class ModelDetailView(APIView):
    def get(self, request, model_id):
        try:
            stored_model = models_collection.find_one({"ModelId": model_id}, {"_id": 0})
            if not stored_model:
                return JsonResponse({'error': 'Model not found'}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'model': stored_model}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching model details: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get manufacturers from MongoDB
class ManufacturerListView(APIView):
    def get(self, request):
        try:
            stored_manufacturers = list(manufacturers_collection.find({}, {"_id": 0}))
            total = len(stored_manufacturers)
            if stored_manufacturers:
                return JsonResponse({
                    'manufacturers': stored_manufacturers,
                    'total': total,
                    'last_updated': stored_manufacturers[0]["last_updated"] if stored_manufacturers else None
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching manufacturers from MongoDB: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get single manufacturer with ID
class ManufacturerDetailView(APIView):
    def get(self, request, manufacturer_id):
        try:
            stored_manufacturer = manufacturers_collection.find_one({"ManufacturerId": manufacturer_id}, {"_id": 0})
            if not stored_manufacturer:
                return JsonResponse({'error': 'Manufacturer not found'}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'manufacturer': stored_manufacturer}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching manufacturer details: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Serve controllers from MongoDB
class ControllerListView(APIView):
    def get(self, request):
        force_update = request.GET.get('force_update', 'false').lower() == 'true'

        if force_update:
            update_controllers()
            stored_controllers = list(controllers_collection.find({}, {"_id": 0}))
            total = len(stored_controllers)
            return JsonResponse({
                'controllers': stored_controllers,
                'total': total,
                'last_updated': stored_controllers[0]["last_updated"] if stored_controllers else None,
                'message': 'Controllers updated manually'
            }, status=status.HTTP_200_OK)

        try:
            stored_controllers = list(controllers_collection.find({}, {"_id": 0}))
            total = len(stored_controllers)
            return JsonResponse({
                'controllers': stored_controllers,
                'total': total,
                'last_updated': stored_controllers[0]["last_updated"] if stored_controllers else None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching controllers from MongoDB: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get single controller with ID
class ControllerDetailView(APIView):
    def get(self, request, controller_id):
        try:
            controller = controllers_collection.find_one({"ControllerId": controller_id}, {"_id": 0})
            if not controller:
                return JsonResponse({'error': 'Controller not found'}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'controller': controller}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching controller details: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

### Rooms
# Serve rooms from MongoDB with optional manual update
class RoomListView(APIView):
    def get(self, request):
        force_update = request.GET.get('force_update', 'false').lower() == 'true'

        if force_update:
            update_rooms()
            stored_rooms = list(rooms_collection.find({}, {"_id": 0}))
            total = len(stored_rooms)
            return JsonResponse({
                'rooms': stored_rooms,
                'total': total,
                'last_updated': stored_rooms[0]["last_updated"] if stored_rooms else None,
                'message': 'Rooms updated manually'
            }, status=status.HTTP_200_OK)

        try:
            stored_rooms = list(rooms_collection.find({}, {"_id": 0}))
            total = len(stored_rooms)
            return JsonResponse({
                'rooms': stored_rooms,
                'total': total,
                'last_updated': stored_rooms[0]["last_updated"] if stored_rooms else None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching rooms from MongoDB: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get single room with ID
class RoomDetailView(APIView):
    def get(self, request, room_id):
        try:
            room = rooms_collection.find_one({"RoomId": room_id}, {"_id": 0})
            if not room:
                return JsonResponse({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'room': room}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching room details: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

### Locations
# Serve locations from MongoDB with optional manual update
class LocationListView(APIView):
    def get(self, request):
        force_update = request.GET.get('force_update', 'false').lower() == 'true'

        if force_update:
            update_locations()
            stored_locations = list(locations_collection.find({}, {"_id": 0}))
            total = len(stored_locations)
            return JsonResponse({
                'locations': stored_locations,
                'total': total,
                'last_updated': stored_locations[0]["last_updated"] if stored_locations else None,
                'message': 'Locations updated manually'
            }, status=status.HTTP_200_OK)

        try:
            stored_locations = list(locations_collection.find({}, {"_id": 0}))
            total = len(stored_locations)
            return JsonResponse({
                'locations': stored_locations,
                'total': total,
                'last_updated': stored_locations[0]["last_updated"] if stored_locations else None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching locations from MongoDB: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get single location with ID
class LocationDetailView(APIView):
    def get(self, request, location_id):
        try:
            location = locations_collection.find_one({"LocationId": location_id}, {"_id": 0})
            if not location:
                return JsonResponse({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({'location': location}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching location details: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

### Treeview
# Serve treeview from MongoDB
class TreeView(APIView):
    def get(self, request):
        force_update = request.GET.get('force_update', 'false').lower() == 'true'
        
        if force_update:
            update_treeview()
            stored_treeview = list(treeview_collection.find({}, {"_id": 0}))
            total = len(stored_treeview)
            return JsonResponse({
                'treeview': stored_treeview,
                'total': total,
                'last_updated': stored_treeview[0]["last_updated"] if stored_treeview else None,
                'message': 'Treeview updated manually'
            }, status=status.HTTP_200_OK)
            
        try:
            stored_treeview = list(treeview_collection.find({}, {"_id": 0}))
            total = len(stored_treeview)
            return JsonResponse({
                'treeview': stored_treeview,
                'total': total,
                'last_updated': stored_treeview[0]["last_updated"] if stored_treeview else None
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching treeview from MongoDB: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
            
# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(update_devices, 'cron', hour=1, minute=0, timezone='America/Chicago')  # Runs daily at 1:00 AM CDT
scheduler.add_job(update_controllers, 'cron', hour=1, minute=0, timezone='America/Chicago')  # Runs daily at 1:00 AM CDT
scheduler.add_job(update_rooms, 'cron', hour=1, minute=0, timezone='America/Chicago')  # Runs daily at 1:00 AM CDT
scheduler.add_job(update_locations, 'cron', hour=1, minute=0, timezone='America/Chicago')  # Runs daily at 1:00 AM CDT
scheduler.add_job(update_treeview, 'cron', hour=1, minute=0, timezone='America/Chicago')  # Runs daily at 1:00 AM CDT

scheduler.start()

# Shut down scheduler when the application exits
atexit.register(lambda: scheduler.shutdown())
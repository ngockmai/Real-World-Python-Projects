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
                    "MaxFilterHours": live_status.get("MaxFilterHours")
                },
                "ControllerCommandGuid": device.get("ControllerCommandGuid")
            }
            devices_collection.update_one(
                {"DeviceId": device.get("DeviceId")},
                {"$set": device_doc},
                upsert=True
            )
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
                "FirmwareVersion": controller.get("FirmwareVersion")
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
            }
            rooms_collection.update_one(
                {"RoomId": room.get("RoomId")},
                {"$set": room_doc},
                upsert=True
            )
        logger.info(f"Rooms updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CDT")
    except requests.RequestException as e:
        logger.error(f"Scheduled update failed - Error fetching rooms: {str(e)}")

# Serve devices from MongoDB
class DeviceListView(APIView):
    def get(self, request):
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
                # 'last_updated': stored_controllers[0]["last_updated"].isoformat() if stored_controllers else None,
                'message': 'Controllers updated manually'
            }, status=status.HTTP_200_OK)

        try:
            stored_controllers = list(controllers_collection.find({}, {"_id": 0}))
            total = len(stored_controllers)
            return JsonResponse({
                'controllers': stored_controllers,
                'total': total,
                # 'last_updated': stored_controllers[0]["last_updated"].isoformat() if stored_controllers else None
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
                # 'last_updated': stored_rooms[0]["last_updated"].isoformat() if stored_rooms else None,
                'message': 'Rooms updated manually'
            }, status=status.HTTP_200_OK)

        try:
            stored_rooms = list(rooms_collection.find({}, {"_id": 0}))
            total = len(stored_rooms)
            return JsonResponse({
                'rooms': stored_rooms,
                'total': total,
                # 'last_updated': stored_rooms[0]["last_updated"].isoformat() if stored_rooms else None
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

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(update_devices, 'cron', hour=1, minute=0, timezone='America/Chicago')  # Runs daily at 1:00 AM CDT
scheduler.add_job(update_controllers, 'cron', hour=1, minute=0, timezone='America/Chicago')  # Runs daily at 1:00 AM CDT

scheduler.start()

# Shut down scheduler when the application exits
atexit.register(lambda: scheduler.shutdown())
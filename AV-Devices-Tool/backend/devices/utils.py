import requests
from django.shortcuts import render
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.http import JsonResponse
import logging
from requests.exceptions import RequestException

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
    
def parse_device_name(device_name):
    try:
        parts = device_name.split(' - ')
        manufacturer = parts[0].strip() if parts else 'N/A'
        model_and_version = parts[1] if len(parts) > 1 else ''
        model_and_version = model_and_version.split('(')[0].strip()
        model_parts = model_and_version.split()
        model = model_parts[0] if model_parts else 'N/A'
        firmware = next((part for part in model_parts if part.startswith('v')), 'N/A')
        return manufacturer, model, firmware
    except Exception as e:
        logger.error(f"Error parsing DeviceName '{device_name}': {e}")
        return 'N/A', 'N/A', 'N/A'

def process_devices(devices, location_tree):
    location_map = {item["Location"]["LocationId"]: item["Location"] for item in location_tree}
    room_map = {}
    for item in location_tree:
        for room in item["Rooms"]:
            room_map[room["RoomId"]] = {
                "room_id": room["RoomId"],
                "room_name": room["RoomName"],
                "LocationId": room["LocationId"]
            }
    processed_devices = []
    for device in devices:
        manufacturer, model, firmware = parse_device_name(device.get("DeviceName", "N/A"))
        room_id = device.get("RoomId", "N/A")
        device_id = device.get("DeviceId", "N/A")
        room = room_map.get(room_id)
        location_id = room["LocationId"] if room else None
        building = location_map.get(location_id)
        campus_id = building["ParentLocationId"] if building else None
        campus = location_map.get(campus_id)
        processed_device = {
            "device_id": device_id,
            "room_id": room_id,
            "room_name": room["room_name"] if room else "N/A",
            "building_name": building["LocationName"] if building else "N/A",
            "campus_name": campus["LocationName"] if campus else "N/A",
            "uofm_name": "UofM",
            "status": device.get("LiveStatus", {}).get("DeviceStatus", "N/A"),
            "type": device.get("DeviceType", "N/A"),
            "manufacturer": manufacturer,
            "model": model,
            "firmware": firmware,
            "device_name": device.get("DeviceName", "N/A"),
            "port": f"{device.get('ControllerPortType', 'N/A')} {device.get('ControllerPortNumber', 'N/A')}",
        }
        processed_devices.append(processed_device)
    return processed_devices
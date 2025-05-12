from rest_framework.views import APIView
from rest_framework import status
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from devices.utils import authenticate_session, parse_device_name, process_devices
from devices.models import Device
import requests
from django.conf import settings
import logging
from django.shortcuts import render

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
        return None, f"Authentication failed: {str(e)}"

###  Devices
# Get all devices
class DeviceListView(APIView):
    def get(self, request):
        session, error = authenticate_session()
        if error:
            logger.error(error)
            return JsonResponse({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Fetch devices from GVE API
            devices_url = f"{settings.GVE_API_URL}/devices"
            devices_response = session.get(devices_url, headers={"Accept": "application/json"})
            devices_response.raise_for_status()
            devices_data = devices_response.json()
            devices = devices_data.get("Devices", [])

            
            # Fetch location tree
            treeview_url = f"{settings.GVE_API_URL}/locations/treeview"
            tree_response = session.get(treeview_url, headers={"Accept": "application/json"}, timeout=10)
            tree_response.raise_for_status()
            location_tree = tree_response.json().get("Locations", [])

            # Process devices and save to database
            # TODO: Implement save to database
            processed_devices = process_devices(devices, location_tree)
            
            return JsonResponse({'devices': processed_devices}, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            logger.error(f"Error fetching devices: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get single device with ID
class DeviceDetailView(APIView):
    def get(self, request, device_id):  
        session, error = authenticate_session()
        if error:
            logger.error(error)
            return JsonResponse({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            # Fetch device details
            device_url = f"{settings.GVE_API_URL}/devices/{device_id}"
            device_response = session.get(device_url, headers={"Accept": "application/json"}, timeout=10)
            device_response.raise_for_status()
            device_data = device_response.json()    
            
            return JsonResponse({'device': device_data}, status=status.HTTP_200_OK)
        
        except requests.RequestException as e:
            logger.error(f"Error fetching device details: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Devices by Room
class DeviceByRoomView(APIView):
    def get(self, request, room_id):
        session, error = authenticate_session()
        if error:
            logger.error(error)
            return JsonResponse({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Fetch devices for specific room
            devices_url = f"{settings.GVE_API_URL}/devices/room/{room_id}"
            devices_response = session.get(devices_url, headers={"Accept": "application/json"}, timeout=10)
            devices_response.raise_for_status()
            devices_data = devices_response.json()
            devices = devices_data.get("Devices", [])
            
            # Fetch location tree
            treeview_url = f"{settings.GVE_API_URL}/locations/treeview"
            tree_response = session.get(treeview_url, headers={"Accept": "application/json"}, timeout=10)
            tree_response.raise_for_status()
            location_tree = tree_response.json().get("Locations", [])

            # Process devices and save to database
            # TODO: Implement save to database
            processed_devices = process_devices(devices, location_tree)
            
            return JsonResponse({'devices': processed_devices}, status=status.HTTP_200_OK)
        
        except requests.RequestException as e:
            logger.error(f"Error fetching devices: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeviceByLocationView(APIView):
    def get(self, request, location_id):
        session, error = authenticate_session()
        if error:
            logger.error(error)
            return JsonResponse({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        try:
            # Fetch devices for specific location
            devices_url = f"{settings.GVE_API_URL}/devices/location/{location_id}"
            devices_response = session.get(devices_url, headers={"Accept": "application/json"}, timeout=10)
            devices_response.raise_for_status()
            devices_data = devices_response.json()
            devices = devices_data.get("Devices", [])

            # Fetch location tree
            treeview_url = f"{settings.GVE_API_URL}/locations/treeview"
            tree_response = session.get(treeview_url, headers={"Accept": "application/json"}, timeout=10)
            tree_response.raise_for_status()
            location_tree = tree_response.json().get("Locations", [])

            # Process devices and save to database
            # TODO: Implement save to database
            processed_devices = process_devices(devices, location_tree)

            return JsonResponse({'devices': processed_devices}, status=status.HTTP_200_OK)  
        
        except requests.RequestException as e:
            logger.error(f"Error fetching devices: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
### Locations
# Get all locations
class LocationListView(APIView):
    def get(self, request):
        session, error = authenticate_session()
        if error:
            logger.error(error)
            return JsonResponse({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Fetch locations
            locations_url = f"{settings.GVE_API_URL}/locations"
            locations_response = session.get(locations_url, headers={"Accept": "application/json"}, timeout=10)
            locations_response.raise_for_status()
            locations_data = locations_response.json()
            
            return JsonResponse({'locations': locations_data}, status=status.HTTP_200_OK)
        
        except requests.RequestException as e:
            logger.error(f"Error fetching locations: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get location by id
class LocationDetailView(APIView):
    def get(self, request, location_id):
        session, error = authenticate_session()
        if error:
            logger.error(error)
            return JsonResponse({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Fetch location details
            location_url = f"{settings.GVE_API_URL}/locations/{location_id}"
            location_response = session.get(location_url, headers={"Accept": "application/json"}, timeout=10)
            location_response.raise_for_status()
            location_data = location_response.json()
            
            return JsonResponse({'location': location_data}, status=status.HTTP_200_OK)
        
        except requests.RequestException as e:
            logger.error(f"Error fetching location details: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Get treeview
class TreeView(APIView):
    def get(self, request):
        session, error = authenticate_session()
        if error:
            logger.error(error)
            return JsonResponse({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            # Fetch treeview
            treeview_url = f"{settings.GVE_API_URL}/locations/treeview"
            treeview_response = session.get(treeview_url, headers={"Accept": "application/json"}, timeout=10)
            treeview_response.raise_for_status()
            treeview_data = treeview_response.json()
            
            return JsonResponse({'treeview': treeview_data}, status=status.HTTP_200_OK)
        
        except requests.RequestException as e:
            logger.error(f"Error fetching treeview: {str(e)}")
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
        
        
        

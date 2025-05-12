import requests
from django.shortcuts import render
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.http import JsonResponse

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
        print(f"Error parsing DeviceName '{device_name}': {e}")
        return 'N/A', 'N/A', 'N/A'    

def build_tree_structure(location_tree):
    location_map = {item["Location"]["LocationId"]: item["Location"] for item in location_tree}
    
    #Initialize the tree structure: UofM > Campuses > Buildings > Rooms
    tree={"UofM" : {"id": 1, "campuses": {}}}
    
    # Organize locations into campuses and buildings
    for item in location_tree:
        loc = item["Location"]
        if loc["Status"] != "Active":
            continue
        loc_id = loc["LocationId"]
        loc_name = loc["LocationName"]
        parent_id = loc.get("ParentLocationId")
        
        # UofM is the root node
        if loc_id ==1:
            continue
        
        # Campuses: direct children of UofM (ParentLocationId = 1)
        if parent_id == 1:
            if loc_name not in tree["UofM"]["campuses"]:
                tree["UofM"]["campuses"][loc_name] = {"id": loc_id, "buildings": {}}
                
        # Buildings: children of campuses
        elif parent_id in location_map:
            campus = location_map.get(parent_id)
            
            # Skip if the campus is not in the tree structure
            if campus["ParentLocationId"] != 1:
                continue
            campus_name = campus["LocationName"]
            if campus_name not in tree["UofM"]["campuses"]:
                tree["UofM"]["campuses"][campus_name] = {"id": parent_id, "buildings": {}}
            tree["UofM"]["campuses"][campus_name]["buildings"][loc_name] = {"id": loc_id, "rooms": []}
    
    # Add rooms to buildings
    for item in location_tree:
        loc = item["Location"]
        if loc["Status"] != "Active":
            continue
        loc_id = loc["LocationId"]
        loc_name = loc["LocationName"]
        parent_id = loc.get("ParentLocationId")
        rooms = item["Rooms"]
        
        # Skip UofM and campuses (no rooms directly under them)
        if not parent_id or parent_id == 1:
            continue
        
        # Find the campus
        parent_loc = location_map.get(parent_id)
        if not parent_loc or parent_loc["ParentLocationId"] != 1:
            continue
        campus_name = parent_loc["LocationName"]
        
        # Ensure the campuses and buildings exists in the tree structure
        if campus_name not in tree["UofM"]["campuses"]:
            tree["UofM"]["campuses"][campus_name] = {"id": parent_id, "buildings": {}}
        if loc_name not in tree["UofM"]["campuses"][campus_name]["buildings"]:
            tree["UofM"]["campuses"][campus_name]["buildings"][loc_name] = {"id": loc_id, "rooms": []}
            
        # Add rooms to the buildings
        for room in rooms:
            if room["Status"] != "Active":
                continue
            tree["UofM"]["campuses"][campus_name]["buildings"][loc_name]["rooms"].append({
                "room_id": room["RoomId"],
                "room_name": room["RoomName"],              
            })
            
    return tree
    
def process_devices(devices, location_tree):
    # Build mapping for lookup
    location_map = {item["Location"]["LocationId"]: item["Location"] for item in location_tree}
    room_map = {}
    
    for item in location_tree:
        for room in item["Rooms"]:
            room_map[room["RoomId"]] = {
                "room_id": room["RoomId"],
                "room_name": room["RoomName"],
                "LocationId": room["LocationId"]
            }
    # Process devices
    processed_devices = []
    for device in devices:
        DeviceName, Status = parse_device_name(device.get("DeviceName", "N/A"))
        room_id = device.get("RoomId", "N/A")
        device_id = device.get("DeviceId", "N/A")
        
        # Find room details
        room = room_map.get(room_id)
        location_id = room["LocationId"] if room else None
        building = location_map.get(location_id)
        campus_id = building["ParentLocationId"] if building else None
        campus = location_map.get(campus_id)
        
        processed_device = {
        "device_id": device_id,  # For linking to detail page
            "room_id": room_id,
            "room_name": room["RoomName"] if room else "N/A",
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

def get_tree_data(request):
    treeview_url = "https://gve3.ad.umanitoba.ca:443/GVE/api/locations/treeview"
    
    # Authenticate
    session, error = authenticate_session()
    if error:
        return JsonResponse({'error': error}, status=500)

    # Fetch the location tree
    try:
        tree_response = session.get(treeview_url, headers={"Accept": "application/json"})
        tree_response.raise_for_status()
        tree_data = tree_response.json().get("Locations", [])
        tree = build_tree_structure(tree_data)
    except requests.RequestException as e:
        return JsonResponse({'error': f"Failed to fetch location tree from API: {str(e)}"}, status=500)

    return JsonResponse({'tree': tree})

def index(request):
    """Main view to render the initial page with the tree structure."""
    treeview_url = "https://gve3.ad.umanitoba.ca:443/GVE/api/locations/treeview"
    
    # Authenticate
    session, error = authenticate_session()
    if error:
        context = {'tree': {}, 'error_message': error}
        return render(request, 'devices/index.html', context)
    
    # Fetch the location tree
    try:
        tree_response = session.get(treeview_url, headers={"Accept": "application/json"})
        tree_response.raise_for_status()
        tree_data = tree_response.json().get("Locations", [])
        tree = build_tree_structure(tree_data)
    except requests.RequestException as e:
        context = {'tree': {}, 'error_message': f"Failed to fetch location tree from API: {str(e)}"}
        return render(request, 'devices/index.html', context)

    context = {
        'tree': tree,
        'error_message': None,
        'location_tree': tree_data,  # Pass location_tree for use in other views
    }
    return render(request, 'devices/index.html', context)

def get_devices(request):
    """View to fetch all devices (UofM level)."""
    devices_url = "https://gve3.ad.umanitoba.ca:443/GVE/api/devices"

    # Authenticate
    session, error = authenticate_session()
    if error:
        return JsonResponse({'error': error}, status=500)

    # Fetch devices
    try:
        devices_response = session.get(devices_url, headers={"Accept": "application/json"})
        devices_response.raise_for_status()
        devices_data = devices_response.json()
        devices = devices_data.get("Devices", [])
    except requests.RequestException as e:
        return JsonResponse({'error': f"Failed to fetch devices from API: {str(e)}"}, status=500)

    # Process devices
    return JsonResponse({'devices': devices})

def get_devices_by_location(request, location_id):
    """View to fetch devices for a specific location (campus or building)."""
    devices_url = f"https://gve3.ad.umanitoba.ca:443/GVE/api/devices/location/{location_id}"

    # Authenticate
    session, error = authenticate_session()
    if error:
        return JsonResponse({'error': error}, status=500)

    # Fetch devices
    try:
        devices_response = session.get(devices_url, headers={"Accept": "application/json"})
        devices_response.raise_for_status()
        devices_data = devices_response.json()
        devices = devices_data.get("Devices", [])
    except requests.RequestException as e:
        return JsonResponse({'error': f"Failed to fetch devices from API: {str(e)}"}, status=500)

    # Fetch location tree for mapping
    treeview_url = "https://gve3.ad.umanitoba.ca:443/GVE/api/locations/treeview"
    try:
        tree_response = session.get(treeview_url, headers={"Accept": "application/json"})
        tree_response.raise_for_status()
        location_tree = tree_response.json().get("Locations", [])
    except requests.RequestException as e:
        return JsonResponse({'error': f"Failed to fetch location tree from API: {str(e)}"}, status=500)

    # Process devices
    processed_devices = process_devices(devices, location_tree)
    return JsonResponse({'devices': processed_devices})

def get_devices_by_room(request, room_id):
    """View to fetch devices for a specific room."""
    devices_url = f"https://gve3.ad.umanitoba.ca:443/GVE/api/devices/room/{room_id}"

    # Authenticate
    session, error = authenticate_session()
    if error:
        return JsonResponse({'error': error}, status=500)

    # Fetch devices
    try:
        devices_response = session.get(devices_url, headers={"Accept": "application/json"})
        devices_response.raise_for_status()
        devices_data = devices_response.json()
        devices = devices_data.get("Devices", [])
    except requests.RequestException as e:
        return JsonResponse({'error': f"Failed to fetch devices from API: {str(e)}"}, status=500)

    # Fetch location tree for mapping
    treeview_url = "https://gve3.ad.umanitoba.ca:443/GVE/api/locations/treeview"
    try:
        tree_response = session.get(treeview_url, headers={"Accept": "application/json"})
        tree_response.raise_for_status()
        location_tree = tree_response.json().get("Locations", [])
    except requests.RequestException as e:
        return JsonResponse({'error': f"Failed to fetch location tree from API: {str(e)}"}, status=500)

    # Process devices
    processed_devices = process_devices(devices, location_tree)
    return JsonResponse({'devices': processed_devices})

def device_detail(request, device_id):
    """View to display detailed information about a specific device."""
    device_url = f"https://gve3.ad.umanitoba.ca:443/GVE/api/devices/{device_id}"
    treeview_url = "https://gve3.ad.umanitoba.ca:443/GVE/api/locations/treeview"

    # Authenticate
    session, error = authenticate_session()
    if error:
        context = {'error_message': error}
        return render(request, 'devices/device_detail.html', context)

    # Fetch the device
    try:
        device_response = session.get(device_url, headers={"Accept": "application/json"})
        device_response.raise_for_status()
        device_data = device_response.json()
        device = device_data.get("Device", {})
    except requests.RequestException as e:
        context = {'error_message': f"Failed to fetch device from API: {str(e)}"}
        return render(request, 'devices/device_detail.html', context)

    # Fetch location tree for mapping
    try:
        tree_response = session.get(treeview_url, headers={"Accept": "application/json"})
        tree_response.raise_for_status()
        location_tree = tree_response.json().get("Locations", [])
    except requests.RequestException as e:
        context = {'error_message': f"Failed to fetch location tree from API: {str(e)}"}
        return render(request, 'devices/device_detail.html', context)

    # Process the device
    devices = [device] if device else []
    processed_devices = process_devices(devices, location_tree)
    device_info = processed_devices[0] if processed_devices else {}

    context = {
        'device': device_info,
        'error_message': None,
    }
    return render(request, 'devices/device_detail.html', context)
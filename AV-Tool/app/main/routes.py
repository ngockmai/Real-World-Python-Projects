from flask import render_template
from . import main
from ..models import Device

@main.route('/')
def index():
    devices = Device.query.all()
    
    # Convert devices to a list of dictionaries
    devices_data = []
    for device in devices:
        device_data = {
            'device_id': device.device_id,
            'campus_name': device.room.building.campus.campus_name if device.room and device.room.building and device.room.building.campus else 'N/A',
            'building_name': device.room.building.building_name if device.room and device.room.building else 'N/A',
            'room_number': device.room.room_number if device.room else 'N/A',
            'model_name': device.model_name,
            'category_name': device.category.category_name if device.category else 'N/A',
            'ip_address': device.ip_address,
            'hostname': device.hostname,
            'mac_address': device.mac_address,
            'serial_number': device.serial_number,
            'firmware_version': device.firmware_version,
            'device_link': device.device_link
        }
        devices_data.append(device_data)
        
    return render_template('index.html', devices=devices_data, Device=Device)

@main.route('/device/new', methods=['GET', 'POST'])
def new_device():
    form = DeviceForm()
    form.room_id.choices = [(0, 'None')] + [(room.room_id, f"{room.room_number} (Building: {room.building.building_name}, Campus: {room.building.campus.campus_name})") for room in Room.query.all()]
    form.category_id.choices = [(0, 'None')] + [(category.category_id, category.category_name) for category in Category.query.all()]
    
    if form.validate_on_submit():
        device = Device(
            model_name=form.model_name.data,
            ip_address=form.ip_address.data,
            mac_address=form.mac_address.data,
            hostname=form.hostname.data,
            serial_number=form.serial_number.data,
            firmware_version=form.firmware_version.data,
            device_link=form.device_link.data,
            room_id=form.room_id.data if form.room_id.data != 0 else None,
            category_id=form.category_id.data if form.category_id.data != 0 else None
        )
        db.session.add(device)
        db.session.commit()
        flash('Device created successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('device_form.html', form=form, title='Add New Device')

@main.route('/device/<int:device_id>')
def view_device(device_id):
    device = Device.query.get_or_404(device_id)
    return render_template('view_device.html', device=device)

@main.route('/device/<int:device_id>/edit', methods=['GET', 'POST'])
def edit_device(device_id):
    device = Device.query.get_or_404(device_id)
    form = DeviceForm(obj=device)
    form.room_id.choices = [(0, 'None')] + [(room.room_id, f"{room.room_number} (Building: {room.building.building_name}, Campus: {room.building.campus.campus_name})") for room in Room.query.all()]
    form.category_id.choices = [(0, 'None')] + [(category.category_id, category.category_name) for category in Category.query.all()]
    
    if form.validate_on_submit():
        device.model_name = form.model_name.data
        device.ip_address = form.ip_address.data
        device.mac_address = form.ip_address.data
        device.hostname = form.hostname.data
        device.serial_number = form.serial_number.data
        device.firmware_version = form.firmware_version.data
        device.device_link = form.device_link.data
        device.room_id = form.room_id.data if form.room_id.data != 0 else None
        device.category_id = form.category_id.data if form.category_id.data != 0 else None
        db.session.commit()
        flash('Device updated successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('device_form.html', form=form, title='Edit Device')

@main.route('/device/<int:device_id>/delete', methods=['POST'])
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    flash('Device deleted successfully!', 'success')
    return redirect(url_for('main.index'))
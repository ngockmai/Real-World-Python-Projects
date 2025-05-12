import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DeviceTable = () => {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingDevice, setEditingDevice] = useState(null);
  const [formData, setFormData] = useState({ notes: '', custom_status: '', owner: '' });
  const [roomId, setRoomId] = useState('');
  const [locationId, setLocationId] = useState('');

  const fetchDevices = async (url) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(url);
      if (!response.data.devices) {
        throw new Error('Unexpected response format: "devices" key missing');
      }
      setDevices(response.data.devices);
      console.log('Fetched devices:', response.data.devices);
    } catch (err) {
      setError('Failed to fetch devices: ' + (err.response?.data?.error || err.message));
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDevices('http://localhost:8000/api/devices/');
  }, []);

  const handleFilterByRoom = () => {
    if (roomId) {
      fetchDevices(`http://localhost:8000/api/devices/room/${roomId}/`);
    }
  };

  const handleFilterByLocation = () => {
    if (locationId) {
      fetchDevices(`http://localhost:8000/api/devices/location/${locationId}/`);
    }
  };

  const handleReset = () => {
    setRoomId('');
    setLocationId('');
    fetchDevices('http://localhost:8000/api/devices/');
  };

  const handleEdit = (device) => {
    setEditingDevice(device.device_id);
    setFormData({
      notes: device.notes || '',
      custom_status: device.custom_status || '',
      owner: device.owner || ''
    });
  };

  const handleSave = async (device_id) => {
    try {
      const response = await axios.post(`http://localhost:8000/api/devices/${device_id}/info/`, formData);
      const updatedDevices = devices.map(device =>
        device.device_id === device_id
          ? { ...device, ...formData }
          : device
      );
      setDevices(updatedDevices);
      setEditingDevice(null);
      console.log(`Saved DeviceInfo for ${device_id}:`, response.data);
    } catch (err) {
      setError('Failed to save device info: ' + (err.response?.data?.error || err.message));
      console.error('Save error:', err);
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const getStatusIcon = (status) => {
    if (!status) return <span className="w-3 h-3 bg-gray-400 rounded-full inline-block"></span>;
    return status.toLowerCase().includes('online') ? (
      <span className="w-3 h-3 bg-green-500 rounded-full inline-block"></span>
    ) : (
      <span className="w-3 h-3 bg-red-500 rounded-full inline-block"></span>
    );
  };

  if (loading) return <div className="text-center text-gray-600">Loading...</div>;
  if (error) return <div className="text-center text-red-600">Error: {error}</div>;
  if (!devices.length) return <div className="text-center text-gray-600">No devices found</div>;

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <div className="flex flex-col sm:flex-row justify-between mb-4 gap-4">
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Room ID"
            value={roomId}
            onChange={(e) => setRoomId(e.target.value)}
            className="border border-gve-gray rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gve-blue"
          />
          <button
            onClick={handleFilterByRoom}
            className="bg-gve-blue text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Filter by Room
          </button>
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Location ID"
            value={locationId}
            onChange={(e) => setLocationId(e.target.value)}
            className="border border-gve-gray rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gve-blue"
          />
          <button
            onClick={handleFilterByLocation}
            className="bg-gve-blue text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Filter by Location
          </button>
        </div>
        <button
          onClick={handleReset}
          className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition"
        >
          Reset
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse border border-gve-gray">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gve-gray px-4 py-2 text-left text-sm font-semibold text-gray-700">Status</th>
              <th className="border border-gve-gray px-4 py-2 text-left text-sm font-semibold text-gray-700">Controller IP/Host</th>
              <th className="border border-gve-gray px-4 py-2 text-left text-sm font-semibold text-gray-700">Type</th>
              <th className="border border-gve-gray px-4 py-2 text-left text-sm font-semibold text-gray-700">Manufacturer</th>
              <th className="border border-gve-gray px-4 py-2 text-left text-sm font-semibold text-gray-700">Model</th>
              <th className="border border-gve-gray px-4 py-2 text-left text-sm font-semibold text-gray-700">Device Name</th>
              <th className="border border-gve-gray px-4 py-2 text-left text-sm font-semibold text-gray-700">Port</th>
              <th className="border border-gve-gray px-4 py-2 text-left text-sm font-semibold text-gray-700">Bi-Directional</th>
            </tr>
          </thead>
          <tbody>
            {devices.map(device => (
              <tr key={device.device_id} className="hover:bg-gray-50">
                <td className="border border-gve-gray px-4 py-2 text-sm text-gray-600">{getStatusIcon(device.status)}</td>
                <td className="border border-gve-gray px-4 py-2 text-sm text-gray-600">{device.room_id || 'N/A'}</td>
                <td className="border border-gve-gray px-4 py-2 text-sm text-gray-600">{device.type}</td>
                <td className="border border-gve-gray px-4 py-2 text-sm text-gray-600">{device.manufacturer}</td>
                <td className="border border-gve-gray px-4 py-2 text-sm text-gray-600">{device.model}</td>
                <td className="border border-gve-gray px-4 py-2 text-sm text-gray-600">{device.device_name}</td>
                <td className="border border-gve-gray px-4 py-2 text-sm text-gray-600">{device.port}</td>
                <td className="border border-gve-gray px-4 py-2 text-sm text-gray-600">
                  <span className="w-4 h-4 bg-gray-300 rounded-full inline-block"></span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="text-right text-sm text-gray-600 mt-2">
        Page 1 of 15 | Displaying Devices 1 - 100 of 1481
      </div>
    </div>
  );
};

export default DeviceTable;
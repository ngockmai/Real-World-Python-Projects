import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TreeView = () => {
  const [treeData, setTreeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTree = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/locations/treeview/');
        setTreeData(response.data.treeview.Locations);
      } catch (err) {
        setError('Failed to fetch tree: ' + (err.response?.data?.error || err.message));
      } finally {
        setLoading(false);
      }
    };
    fetchTree();
  }, []);

  const renderLocation = (location) => {
    return (
      <li key={location.Location.LocationId} className="ml-4">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-gray-700">{location.Location.LocationName}</span>
          <span className="text-xs text-gray-500">({location.Location.Status})</span>
        </div>
        {location.Rooms && location.Rooms.length > 0 && (
          <ul className="list-none ml-4">
            {location.Rooms.map(room => (
              <li key={room.RoomId} className="text-sm text-gray-600">
                {room.RoomName} ({room.Category})
              </li>
            ))}
          </ul>
        )}
      </li>
    );
  };

  if (loading) return <div className="text-center text-gray-600">Loading...</div>;
  if (error) return <div className="text-center text-red-600">{error}</div>;
  if (!treeData) return <div className="text-center text-gray-600">No data available</div>;

  // Group locations by parent
  const locationsByParent = treeData.reduce((acc, location) => {
    const parentId = location.Location.ParentLocationId || 'root';
    if (!acc[parentId]) {
      acc[parentId] = [];
    }
    acc[parentId].push(location);
    return acc;
  }, {});

  const renderHierarchy = (parentId = 'root', level = 0) => {
    const locations = locationsByParent[parentId] || [];
    if (locations.length === 0) return null;

    return (
      <ul className={`list-none ${level === 0 ? '' : 'ml-4'}`}>
        {locations.map(location => (
          <li key={location.Location.LocationId}>
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-gray-700">{location.Location.LocationName}</span>
              <span className="text-xs text-gray-500">({location.Location.Status})</span>
            </div>
            {location.Rooms && location.Rooms.length > 0 && (
              <ul className="list-none ml-4">
                {location.Rooms.map(room => (
                  <li key={room.RoomId} className="text-sm text-gray-600">
                    {room.RoomName} ({room.Category})
                  </li>
                ))}
              </ul>
            )}
            {renderHierarchy(location.Location.LocationId, level + 1)}
          </li>
        ))}
      </ul>
    );
  };

  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-4">Location Tree View</h2>
      {renderHierarchy()}
    </div>
  );
};

export default TreeView;
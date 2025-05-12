import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TreeView = () => {
  const [tree, setTree] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTree = async () => {
      try {
        const response = await axios.get('http://localhost:8000/');
        setTree(response.data.tree || {});
      } catch (err) {
        setError('Failed to fetch tree: ' + (err.response?.data?.error || err.message));
      } finally {
        setLoading(false);
      }
    };
    fetchTree();
  }, []);

  if (loading) return <div className="text-center text-gray-600">Loading...</div>;
  if (error) return <div className="text-center text-red-600">{error}</div>;

  const renderTree = (data) => {
    return Object.entries(data).map(([key, value]) => (
      <li key={key} className="ml-4">
        <span className="text-sm text-gray-700">{key}</span>
        {value.campuses && (
          <ul className="list-none">
            {renderTree(value.campuses)}
          </ul>
        )}
        {value.buildings && (
          <ul className="list-none">
            {Object.entries(value.buildings).map(([building, buildingData]) => (
              <li key={building} className="ml-4">
                <span className="text-sm text-gray-700">{building}</span>
                {buildingData.rooms && (
                  <ul className="list-none">
                    {buildingData.rooms.map(room => (
                      <li key={room.room_id} className="ml-4 text-sm text-gray-600">
                        {room.room_name} (ID: {room.room_id})
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ul>
        )}
      </li>
    ));
  };

  return (
    <div className="space-y-2">
      <ul className="list-none">{renderTree(tree)}</ul>
    </div>
  );
};

export default TreeView;
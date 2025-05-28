import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import {
  useReactTable,
  getCoreRowModel,
  flexRender
} from '@tanstack/react-table';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Accept only locationType and locationId
export default function DeviceTable({ locationType, locationId }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!locationType || locationId === undefined || locationId === null) {
      setData([]);
      setLoading(false);
      setError(null);
      return;
    }

    const fetchDevices = async () => {
      setLoading(true);
      setError(null);
      try {
        const endpointType = locationType === 'room' ? 'room' : 'location';
        const url = `${API_BASE_URL}/devices/${endpointType}/${locationId}`;
        
        console.log("DeviceTable: Fetching devices from:", url);

        const response = await axios.get(url);
        setData(response.data.devices || []);
      } catch (err) {
        console.error("DeviceTable: Failed to fetch devices:", err);
        setError(err.response?.data?.error || err.message || 'Failed to fetch devices');
        setData([]);
      } finally {
        setLoading(false);
      }
    };

    fetchDevices();
  }, [locationType, locationId]); // Dependencies remain the same

  const columns = useMemo(() => [
    { header: 'Room', accessorKey: 'RoomName' },
    { header: 'Status', accessorKey: 'Status' },
    { header: 'Power', accessorKey: 'Power' },
    { header: 'Controller Host', accessorKey: 'ControllerHost' },
    { header: 'Type', accessorKey: 'Type' }, // Device Type
    { header: 'Manufacturer', accessorKey: 'Manufacturer' },
    { header: 'Model', accessorKey: 'Model' },
    { header: 'Device Name', accessorKey: 'DeviceName' },
    { header: 'Port', accessorKey: 'Port' },
  ], []);

  const tableInstance = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  // Initial state before any selection from the tree
  if (!locationType && (locationId === undefined || locationId === null)) {
    return (
      <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow h-full flex items-center justify-center">
        <p className="text-gray-600 dark:text-gray-400">Select a location or room to view devices.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow h-full flex items-center justify-center">
        {/* Updated loading message */}
        <p className="text-gray-600 dark:text-gray-400">Loading devices for {locationType} ID: {locationId}...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-100 text-red-700 rounded-lg shadow dark:bg-red-900/30 dark:text-red-300">
        {/* Updated error message */}
        <p className="font-semibold">Error loading devices for {locationType} ID: {locationId}:</p>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow h-full flex flex-col">
      <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">
        {/* Updated title */}
        Devices for {locationType.charAt(0).toUpperCase() + locationType.slice(1)} ID: {locationId}
      </h2>
      {data.length > 0 ? (
        <div className="overflow-x-auto flex-1">
          <table className="w-full border-collapse text-sm">
            <thead className="sticky top-0 bg-gray-100 dark:bg-gray-700 z-10">
              {tableInstance.getHeaderGroups().map(headerGroup => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map(header => (
                    <th
                      key={header.id}
                      colSpan={header.colSpan}
                      className="border p-2 text-left font-semibold text-gray-700 dark:text-gray-200 dark:border-gray-600"
                    >
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {tableInstance.getRowModel().rows.map(row => (
                <tr key={row.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                  {row.getVisibleCells().map(cell => (
                    <td key={cell.id} className="border p-2 text-gray-700 dark:text-gray-300 dark:border-gray-600">
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      ) ?? <span className="text-gray-400 dark:text-gray-500">N/A</span>}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-gray-600 dark:text-gray-400 mt-4">
          {/* Updated no data message */}
          No devices found for {locationType} ID: {locationId}.
        </p>
      )}
    </div>
  );
}
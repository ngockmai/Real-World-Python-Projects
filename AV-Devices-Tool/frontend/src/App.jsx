import React, {useState, useEffect } from 'react'
import TreeView from './TreeView'
import DeviceTable from './DeviceTable'
import './App.css'

// Mock tree data for development
const mockTreeData = {
    UofM: {
        id: 1,
        campuses: {
            "Bannatyne": {
            id: 2,
            buildings: {
                "Apotex": {
                id: 101,
                rooms: [
                    { room_name: "Apotex 050", room_id: 201 }
                ]
                },
                "BMS": {
                id: 102,
                rooms: [
                    { room_name: "BMS 202", room_id: 202 }
                ]
                }
            }
            },
            "Fort Garry": {
            id: 3,
            buildings: {
                "Admin": {
                id: 103,
                rooms: [
                    { room_name: "Admin 100", room_id: 246 }
                ]
                }
            }
            }
        }
    }
  };
  
  // Mock device data for development
const mockDevices = [
{
    device_id: 1,
    room_name: "Apotex 050",
    status: "On",
    model: "Model X",
    device_name: "Device 1"
},
{
    device_id: 2,
    room_name: "BMS 202",
    status: "Off",
    model: "Model Y",
    device_name: "Device 2"
}
];

const App = () => {
    const [devices, setDevices] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const treeData = mockTreeData
    console.log('treeData:', treeData)
    console.log('devices', mockDevices)

    // const fetchTreeData = () => {
    //     fetch('/tree-data/')
    //     .then(response => response.json())
    //     .then(data => {
    //         if(data.error){
    //             setError(data.error)
    //         } else{
    //             setTreeData(data.tree)
    //         }      
    //     })
    //     .catch(err => {
    //         setError('Error fetching tree data: ' + err.message)
    //     })
    // }
    const fetchDevices = (filterType, filterValue, filterId) => {
        setLoading(true)
        setError(null)

        setTimeout(() => {
            setLoading(false)
            setDevices(mockDevices)
        }, 500)

        // let url;
        // if (filterType == 'uofm'){
        //     url = "/devices/"
        // } else if (filterType === 'campus' || filterType === 'building'){
        //     url = `devices/location/${filterId}`
        // } else if (filterType === 'room') {
        //     url = `/devices/room/${filterValue}/`
        // }

        // fetch(url)
        //     .then(response => response.json())
        //     .then(data => {
        //         setLoading(false)
        //         if (data.error) {
        //             setError(data.error)
        //             setDevices([])
        //         } else{
        //             setDevices(data.devices)
        //         }
        //     })
        //     .catch(err => {
        //         setLoading(false)
        //         setError('Error fetching devices: ' + err.message)
        //         setDevices([])
        //     })       
    }

    useEffect(() => {
        // Initially fetch all devices at UoM level
        fetchDevices('UofM', 1, 1)
    }, [])

    return (
        <div className="min-h-screen flex flex-col">
        <div className="flex flex-1 flex-col md:flex-row p-4">
            <div className="w-full md:w-1/4 p-4">
            <h5 className="text-lg font-semibold mb-2">GVE Location Tree</h5>
            <TreeView treeData={treeData} onNodeClick={fetchDevices} />
            </div>
            <div className="w-full md:w-3/4 p-4">
            <h1 className="text-2xl font-bold mb-4">Devices</h1>
            {loading && <div className="text-gray-500 italic mb-2">Loading devices...</div>}
            {error && <div className="bg-red-100 text-red-700 p-2 rounded mb-2">{error}</div>}
            <DeviceTable devices={devices} />
            </div>
        </div>
        <footer className="mt-auto p-4 border-t border-gray-200 text-center text-gray-600">
            <p>© 2023 AV-Tool. All rights reserved.</p>
        </footer>
        </div>
    )
}

export default App
import React, { useState, useEffect, useCallback, useRef, useLayoutEffect } from "react";
import axios from 'axios'
import { Tree } from 'react-arborist'
import { Button } from "@/components/ui/button"
import {Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Skeleton } from '@/components/ui/skeleton'
import { RefreshCw, ListTree, AlertTriangle, Info } from 'lucide-react'


// Config
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

/**
 * 
 * @param {object} item - the source data item (campuses, buildings, rooms) 
 * @param {string} type - identifies the type of the item (campus, building, room)
 * @param {string} idKey - the key in `item` that identifies the item uniquely
 * @param {string} nameKey - the key in `item` that contains the name of the item
 * @param {string} [childrenKey] - the key in `item` for the array of children
 * @param {function} [childrenProcessor] - a function that processes the children of the item
 * @param {boolean} [initiallyOpen] - whether the node should be initially open
 * @returns {object|null} A react-arborist node object or null if the item is not valid
 */

const createArboristNode = (item, type, idKey, nameKey, childrenKey, childrenProcessor) => {
    if (!item || item[idKey] === undefined){
        console.warn(`Skipping node creation for ${item}: item missing ${idKey}`, item)
        return null
    }

    const nodeId = `${type}-${item[idKey]}`
    const node = {
        id: nodeId,
        name: `${item[nameKey] || 'Unknown Name'}`,
        data: {
            type,
            id: item[idKey],
            data: { ...item, originalType: type },
            children: null,
        }
    }

    if (childrenKey && item[childrenKey] && Array.isArray(item[childrenKey])){
        if (item[childrenKey].length > 0 && childrenProcessor){
            node.children = item[childrenKey].map(child => childrenProcessor(child)).filter(Boolean)
        } else{
            node.children = []
        }
    }
    else if (!childrenKey){
        node.children = []
    }


    return node
}

/**
 * 
 * Transform the tree data into a format that can be used by react-arborist
 * 
 * @param {object} apiResponse - the raw tree data
 * @returns {Array} an array containing the root node for react-arborist
 */
const transformTreeData = (apiResponse) => {
    if (!apiResponse || !apiResponse.treeview){
        console.warn('No tree data found', apiResponse)
        return []
    }

    const rootApiNode = apiResponse.treeview

    const processRoomNode = (room) => 
        createArboristNode(room, 'room', 'RoomId', 'RoomName')

    const processBuildingNode = (building) => 
        createArboristNode(building, 'bldg', 'LocationId', 'LocationName', 'Rooms', processRoomNode)

    const processCampusNode = (campus) => 
        createArboristNode(campus, 'camp', 'LocationId', 'LocationName', 'Buildings', processBuildingNode)

    const rootNode = createArboristNode(rootApiNode, 'loc', 'LocationId', 'LocationName', 'Campuses', processCampusNode)

    return rootNode ? [rootNode] : []
}

const LocationTree = () => {
    const [treeData, setTreeData] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [lastUpdated, setLastUpdated] = useState(null)

    const fetchTreeData = useCallback(async () => {
        setLoading(true)
        setError(null)
        
        try{
            const url = `${API_BASE_URL}/locations/treeview`
            const response = await axios.get(url)
            const apiData = response.data

            if (apiData && apiData.treeview){
                setTreeData(transformTreeData(apiData))
                setLastUpdated(apiData.lastUpdated || 'N/A')
                if (apiData.message){
                    console.info("Server message:", apiData.message)
                }
            } else {
                console.error('Received empty or invalid tree data from server:', apiData)
                setError('received empty or invalid tree data from server')
                setTreeData([])
                setLastUpdated(null)
            }
        } catch(err){
            console.error('Failed to fetch tree data:', err)
            const errorMessage = err.response?.data?.error || err.message || 'Unknown error'
            setError(`Failed to fetch tree data: ${errorMessage}`)
            setTreeData([])
            setLastUpdated(null)
        } finally {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        fetchTreeData()
    }, [fetchTreeData])
    
    // Define initial open state
    const initialOpenState = {}
    const setInitialOpenState = (nodes) => {
        nodes.forEach((node) => {
            if (node.data.type === 'loc' || node.data.type === 'camp'){
                initialOpenState[node.id] = true
            }
            if (node.children){
                setInitialOpenState(node.children)
            }
        })
    }

    if(treeData.length > 0){
        setInitialOpenState(treeData)
    }

    if (loading && treeData.length === 0){
        return (
            <div className="p-4 text-center">
                <p>Loading location tree...</p>
            </div>
        )
    }

    if (error && treeData.length === 0){
        return (
            <div className="p-4 text-red-700 bg-red-100 border border-red-300 rounded-md">
                <p className="font-semibold text-lg">Error Occurred</p>
                <p>{error}</p>
                <Button onClick={fetchTreeData} className="mt-3">Try Again</Button>
            </div>
        )
    }

    return (
        <div className="p-4 bg-white shadow-md rounded-lg h-full flex flex-col">
            <div className="flex flex-wrap justify-between items-center mb-4 gap-2">
                <h1 className="text-2xl font-semibold text-gray-800">Location Tree</h1>
            </div>

            {error && !loading && (
                <div className="mb-4 p-3 text-sm text-red-700 bg-red-100 border border-red-300 rounded-md">
                    <p><span className="font-semibold">Refresh Error:</span> {error}</p>
                </div>
            )}

            {treeData.length > 0 ? (
                <div 
                className="flex-1 overflow-auto" 
                style={{
                    height: 'calc(100vh - 200px)',
                    maxWidth: '400px',
                    minHeight: '400px',
                    border: '1px solid #e2e8f10',
                    borderRadius: '0.25rem'
                }}>
                    <Tree 
                    data={treeData}
                    className="h-ful w-full"
                    initialOpenState={initialOpenState}
                    openByDefault = {false}
                    />
                </div>
                    
            ) : (
                !loading && <p className="text-gray-600">No location data available to display.</p>
            )}
        </div>
    )
}

export default LocationTree
import React, { useState } from "react"
import LocationTree from "./location-tree"
import DeviceTable from "./device-table"
import Header from "./header"

export default function Homepage() {
    const [selectedNodeInfo, setSelectedNodeInfo] = useState(null)
    
    const handleNodeSelect = (node) => {
        console.log('Node data:', node.data.data)
        if(node && node.data && node.data.data){
            const {type, originalId, name, apiData} = node.data.data
            console.log('type:', type, 'originalId:', originalId, 'name:', name, 'apiData:', apiData)
            setSelectedNodeInfo({
                arboristNodeId: node.id,
                type: type,
                originalId: originalId,
                name: name,
                apiData: apiData
            })
        } else {
            setSelectedNodeInfo(null)
        }
        
    }

    return (
        <div className="flex min-h-screen flex-col">
            <Header />       
            <div className="flex flex-1 flex-row gap-4 p-4">
                <LocationTree 
                    onNodeSelect={handleNodeSelect} 
                    selectedNode={selectedNodeInfo ? {id: selectedNodeInfo.originalId} : null}
                    />
                <div className="flex-1 rounded-xl bg-muted/50 p-4">
                    {selectedNodeInfo ? (
                        <DeviceTable 
                        locationType={selectedNodeInfo.type}
                        locationId={selectedNodeInfo.originalId} 
                    />
                    ) : (
                        <p className="text-center text-muted-foreground">
                            Select an item from the location tree to see details.
                        </p> 
                    )}
                </div>
            </div>
            <div className="flex-1 rounded-xl bg-muted/50 p-4">
                <p className="text-center text-muted-foreground">Footer goes here</p>
            </div>
        </div>
        
    )
}
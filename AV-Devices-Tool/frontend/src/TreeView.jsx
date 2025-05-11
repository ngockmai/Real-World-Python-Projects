import React, {useState} from 'react'
const TreeView = ({treeData, onNodeClick}) => {
    const [expandedNodes, setExpandedNodes] = useState({})
    const toggleNode = (nodeId) => {
        setExpandedNodes(prev => ({
            ...prev,
            [nodeId]: !prev[nodeId]
        }))
    }
    const handleNodeClick = (filterType, filterValue, filterId) => {
        onNodeClick(filterType, filterValue, filterId)
    }

    const renderTree = (node, type, value, id) => {
        if (!node) return null

        if (type === 'uofm'){
            const uofm = node.UofM
            return (
                <ul className='tree'>
                    <li>
                        <a
                        className={expandedNodes['uofm'] ? 'expanded' : ''}
                        onClick={() => {
                            toggleNode('uofm')
                            handleNodeClick('uofm', uofm.id, uofm.id)
                        }}
                        >
                            UofM
                        </a>
                        {expandedNodes['uofm'] && (
                            <ul>
                                {Object.entries(uofm.campuses).map(([campusName, campusData]) => (
                                    <li key={campusName}>
                                        <a
                                            className={expandedNodes[campusName] ? 'expanded' : ''}
                                            onClick = {() => {
                                                toggleNode(campusName)
                                                handleNodeClick('campus', campusName, campusData.id)
                                            }}
                                            >
                                            {campusName}
                                        </a>
                                        {expandedNodes[campusName] && (
                                            <ul>
                                                {Object.entries(campusData.buildings).map(([buildingName, buildingData]) => (
                                                    <li key={buildingName}>
                                                        <a
                                                            className={expandedNodes[buildingName] ? 'expanded' : ''}
                                                            onClick={ () => {
                                                                toggleNode(buildingName)
                                                                handleNodeClick('building', buildingName, buildingData.id)
                                                            }}
                                                            >
                                                            {buildingName}
                                                        </a>
                                                        {expandedNodes[buildingName] && (
                                                            <ul>
                                                                {buildingData.rooms.map(room => (
                                                                    <li key={room.room_id}>
                                                                        <a
                                                                        onClick={() => handleNodeClick('room', room.room_id, room.room_id)}
                                                                        >
                                                                            {room.room_id}
                                                                        </a>
                                                                    </li>
                                                                ))}
                                                            </ul>
                                                        )}
                                                    </li>
                                                ))}
                                            </ul>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </li>
                </ul>
            )
        }
    return null
    }

    return <div>{renderTree(treeData, 'uofm', null, null)}</div>
}

export default TreeView
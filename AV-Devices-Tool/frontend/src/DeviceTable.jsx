import React from 'react'

const DeviceTable = ({devices}) => {
    return (
        <table className='table table-striped table-bordered table-responsive-sm'>
            <thead className='table-dark'>
                <tr>
                    <th scope='col'>Room Name</th>
                    <th scope='col'>Status</th>
                    <th scope='col'>Model</th>
                    <th scope='col'>Device Name</th>
                </tr>
            </thead>
            <tbody className='table-group-divider'>
                {devices.length === 0 ? (
                    <tr>
                        <td colSpan='4'>No devices found</td>
                    </tr>
                ) : (
                    devices.map(device => (
                        <tr key={device.device_id}>
                            <td>{device.room_name || 'N/A'}</td>
                            <td>
                                <span className={`status-dot ${device.status === 'On' ? 'status-on' : device.status === 'Off' ? 'status-off' : 'status-unknown'}`}></span>
                                {device.status || 'N/A'}
                            </td>
                            <td>{device.model || 'N/A'}</td>
                            <td>
                                <a href={`/device/${device.device_id}/`}>{device.device_name || 'N/A'}</a>
                            </td>
                        </tr>
                    ))
                )}

            </tbody>
        </table>
    )
}

export default DeviceTable
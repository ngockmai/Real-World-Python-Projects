import React from 'react';
import TreeView from './components/TreeView';
import DeviceTable from './components/DeviceTable';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <header className="bg-gve-blue text-white p-2 flex justify-between items-center shadow-md">
        <div className="flex items-center">
          <span className="text-lg font-bold">GlobalViewer Enterprise</span>
          <span className="ml-2 text-sm">2.8.6</span>
        </div>
        <div className="flex space-x-4">
          <span>Help Desk</span>
          <span>Scheduling</span>
          <span>Monitoring</span>
          <span>Reporting</span>
          <span>System Menu</span>
          <span>User Preferences</span>
        </div>
        <div className="text-sm">Logged in as: main1</div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-1/4 bg-white shadow-md p-4">
          <div className="mb-4">
            <input
              type="text"
              placeholder="Search for a Room"
              className="w-full border border-gve-gray rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gve-blue"
            />
          </div>
          <TreeView />
        </aside>

        {/* Main Panel */}
        <main className="w-3/4 p-4">
          <DeviceTable />
        </main>
      </div>
    </div>
  );
}

export default App;
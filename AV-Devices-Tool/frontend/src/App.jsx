import React from 'react';
import TreeView from './components/TreeView';
import DeviceTable from './components/DeviceTable';
import Header from './components/Header';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <Header />

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
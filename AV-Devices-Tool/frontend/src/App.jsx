import React from 'react';
import TreeView from './components/TreeView';
import DeviceTable from './components/DeviceTable';
import Header from './components/Header';
import Navigation from './components/Navigation';
import './index.css';
import { Button } from "@/components/ui/button";
import { ChevronDown, ChevronRight, HelpCircle, Info, Plus, Search } from "lucide-react"

function App() {
  return (
    <div className="flex flex-col h-screen bg-white">

      {/* Header */}
      <header className="flex items-center justify-between px-4 py-1 bg-[#1e4b7a] text-white border-b border-gray-300">
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-bold">GlobalViewer Enterprise</h1>
          <span className="text-sm ml-2">7.0.5</span>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span>English (US)</span>
          </div>
          <div className="flex flex-col items-end">
            <span className="text-xs">Logged in as: main1</span>
            <Button variant="secondary" size="sm" className="h-6 text-xs px-2 py-0">
              Log out
            </Button>
          </div>
        </div>
      </header>

      {/* Navigation - Full width background with centered content */}
      <div className="bg-white border-b border-gray-300 w-full">
        <div className="mx-auto w-full">
          <Navigation />
        </div>
      </div>
      
      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">

        {/* Left Panel - Tree View */}
        <div className="w-[230px] border-r border-gray-300 bg-gray-100">
          <div className="p-2 bg-gray-200 border-b border-gray-300 flex justify-between items-center">
            <div className="flex items-center">
              <select className="text-sm bg-transparent border-none outline-none">
                <option> Select a Room</option>
              </select>
            </div>
          </div>
          <div className="p-1 border-b border-gray-300 bg-gray-200">
            <span className="text-sm">Location Tree</span>
          </div>
          {/* <TreeView /> */}

          <aside className=" bg-gray-100 p-4 overflow-y-auto h-[calc(100vh-180px)]">
          <h2 className="font-semibold mb-4">GVE Location Tree</h2>
          <ul className="text-sm space-y-1">
            <li>UofM
              <ul className="pl-4">
                <li>Bannatyne
                  <ul className="pl-4">
                    <li>Apotex</li>
                    <li>BMS</li>
                    <li>Brodie</li>
                  </ul>
                </li>
                <li>Fort Garry
                  <ul className="pl-4">
                    <li>Allen
                      <ul className="pl-4">
                        <li>Allen 319</li>
                        <li>Allen 330</li>
                      </ul>
                    </li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
        </aside>
        </div>

        {/* Main Panel */}
        <main className="w-3/4 p-4">
          <DeviceTable />
        </main>
      </div>
    </div>
  );
}

export default App;
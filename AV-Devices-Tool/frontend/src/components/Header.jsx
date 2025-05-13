import React from "react";

export default function Header() {
    return (
        <header className="bg-blue-900 text-white flex items-center justify-between px-6 py-2">
        <div className="flex items-center gap-2">
            <span className="text-2xl font-bold">AV Devices Tool</span>
        </div>
        <div>
            <span>Logged in as: <b>main1</b></span>
            <button className="ml-4 bg-blue-700 px-2 py-1 rounded">Log out</button>
        </div>
        </header>
    );
}
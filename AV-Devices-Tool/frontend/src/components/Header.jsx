import React from "react";
import { Button } from "@/components/ui/button";

export default function Header() {
    return (
        <header className="flex items-center justify-between py-1 px-8 text-white">
            <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold">AV Devices Tool</h1>
                <span className="text-sm ml-2">1.0.0</span>
            </div>
            <div className="flex items-center gap-4">
                <span className="text-xs mr-2">Logged in as: <strong>admin</strong></span>
                <Button variant="secondary">Logout</Button>
            </div>
        </header>
    );
}
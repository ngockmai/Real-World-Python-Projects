export default function Navigation() {
    return (
        <nav className="flex py-2">
            {/* Navigation bar */}
            <div className="flex gap-6">
                <a href="#" className="font-medium px-2 py-1 border-b-2 border-gray-300">Dashboard</a>
                <a href="#" className="px-2 py-1 hover:border-b-2 hover:border-gray-300">Settings</a>
            </div>
        </nav>
    )
}
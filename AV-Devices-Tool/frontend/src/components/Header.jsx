import { Sheet, SheetTrigger, SheetContent } from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import { NavigationMenu, NavigationMenuList, NavigationMenuLink } from "@/components/ui/navigation-menu"
import { Link } from "react-router-dom"
import { MenuIcon } from "lucide-react"

const navigationItems = [
    { name: "Dashboard", path: "/" },
    { name: "Settings", path: "/settings" },
]

export default function Header() {
    return (
        <header className="flex h-20 w-full shrink-0 items-center px-4 md:px-6 border-b">
        <Link to={"/"} className="flex items-center gap-2 font-semibold text-xl p-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-md bg-primary text-primary-foreground">
            AV
        </div>
        <span className="text-xl font-semibold">Devices Tool</span>
        </Link>
        <Sheet>
            <SheetTrigger asChild>
            <Button variant="outline" size="icon" className="lg:hidden">
                <MenuIcon className="h-6 w-6" />
                <span className="sr-only">Toggle navigation menu</span>
            </Button>
            </SheetTrigger>
            <SheetContent side="left">
            <nav className="flex flex-col gap-4">
                {navigationItems.map((item) => (
                <Link
                    key={item.name}
                    to={item.path}
                    className="text-sm font-medium hover:underline"
                >
                    {item.name}
                </Link>
                ))}
            </nav>
            </SheetContent>
        </Sheet>
        
        <NavigationMenu className="hidden lg:flex">
            <NavigationMenuList>
            {navigationItems.map((item) => (
                <NavigationMenuLink key={item.name} asChild>
                <Link
                    to={item.path}
                    className="group inline-flex h-9 w-max items-center justify-center rounded-md bg-white px-4 py-2 text-sm font-medium transition-colors hover:bg-gray-100 hover:text-gray-900 focus:bg-gray-100 focus:text-gray-900 focus:outline-none disabled:pointer-events-none disabled:opacity-50 data-[active]:bg-gray-100/50 data-[state=open]:bg-gray-100/50 dark:bg-gray-950 dark:hover:bg-gray-800 dark:hover:text-gray-50 dark:focus:bg-gray-800 dark:focus:text-gray-50 dark:data-[active]:bg-gray-800/50 dark:data-[state=open]:bg-gray-800/50"
                    prefetch={false}
                >
                    {item.name}
                </Link>
                </NavigationMenuLink>
            ))}
            </NavigationMenuList>
        </NavigationMenu>
        
        <div className="ml-auto flex gap-2 items-center">
            <span>Logged in as: </span>
            <Button variant="outline">Main1</Button>
        </div>
        </header>
    )
}

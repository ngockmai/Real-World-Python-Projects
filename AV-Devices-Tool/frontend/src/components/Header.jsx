import React from "react";
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { NavigationMenu, NavigationMenuList, NavigationMenuLink } from "@/components/ui/navigation-menu"
import { Search, MessageCircle } from "lucide-react"
import { SidebarTrigger } from "@/components/ui/sidebar"
export default function Header() {
    return (
        <header className="sticky top-0 z-50 flex h-16 items-center justify-between border-b bg-background px-4 md:px-6">
            <div className="flex items-center gap-4">
                <div className="md:hidden">
                    <SidebarTrigger />
                </div>
                <a href="/" className="flex items-center gap-2 font-semibold">
                    <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary text-primary-foreground">
                        K
                    </div>
                    <span>Kirimase</span>
                </a>
            </div>

            <div className="hidden flex-1 items-center justify-center px-4 md:flex">
                <div className="relative w-full md:max-w-md lg:max-w-lg">               
                    {/* <input type="search" placeholder="Search..." className="w-full rounded-md border p-2" /> */}
                </div>
            </div>

            <div className="flex items-center gap-2">
                <Button variant="outline" size="sm" className="hidden md:flex">Profile</Button>
                {/* <Button variant="ghost" size="icon" className="md:hidden"><UserIcon className="h-5 w-5" /></Button> */}
            </div>
        </header>
    );
}
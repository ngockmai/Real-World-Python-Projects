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
        </div>
        
        <Sheet>
            <SheetTrigger asChild>
            <Button variant="outline" size="icon" className="lg:hidden">
                <span className="sr-only">Toggle navigation menu</span>
            </Button>
            </SheetTrigger>
            <SheetContent side="left">
            <a href="#" >Home</a>
            <div className="grid gap-2 py-6">
            <a href="#" >Home</a>
            <a href="#" >About</a>
            <a href="#" >Services</a>
            <a href="#" >Portfolio</a>
            <a href="#" >Contact</a>
            </div>
            </SheetContent>
        </Sheet>
        <NavigationMenu className="hidden lg:flex">
            <NavigationMenuList>
            <NavigationMenuLink asChild>
                <a href="#" >Home</a>
            </NavigationMenuLink>
            <NavigationMenuLink asChild>
            <a href="#" >Home</a>
            </NavigationMenuLink>
            <NavigationMenuLink asChild>
                
            </NavigationMenuLink>
            <NavigationMenuLink asChild>
                
            </NavigationMenuLink>
            <NavigationMenuLink asChild>
                
            </NavigationMenuLink>
            </NavigationMenuList>
        </NavigationMenu>
        <div className="ml-auto flex gap-2">
            <Button variant="outline">Sign in</Button>
            <Button>Sign Up</Button>
        </div>
        </header>
    );
}
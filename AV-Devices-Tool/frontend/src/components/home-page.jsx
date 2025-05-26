import LocationTree from "./location-tree"
// import { Separator } from "@/components/ui/separator"
// import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import Header from "./header"
export default function Homepage() {
    return (
        <div className="flex min-h-screen flex-col">
            <Header />       
            <div className="flex flex-1 flex-row gap-4 p-4">
                <LocationTree />
                <div className="flex-1 rounded-xl bg-muted/50 p-4">                
                    {/* Data table */}
                    <p className="text-center text-muted-foreground">Data Table goes here</p>
                </div>
            </div>
            <div className="flex-1 rounded-xl bg-muted/50 p-4">
                <p className="text-center text-muted-foreground">Footer goes here</p>
            </div>
        </div>
        
    )
}
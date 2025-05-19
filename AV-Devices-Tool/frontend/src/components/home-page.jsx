import {SidebarProvider} from '@/components/ui/sidebar'
import Header from './Header'
import AppSidebar from './sidebar'
import MainContent from './main-content'
export default function Homepage() {
    return (
        <SidebarProvider>
            <div className="flex min-h-screen flex-col">
                <Header />
                <div className="flex flex-1">
                    <AppSidebar />
                    <MainContent />
                </div>
            </div>
        </SidebarProvider>
    )
}
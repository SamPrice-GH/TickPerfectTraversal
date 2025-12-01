import "./globals.css";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"

export const metadata = {
  title: "Tick Perfect Traversal",
  description: "A backtesting engine for algorithmic trading strategies.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex min-h-screen bg-gray-100">
        <SidebarProvider defaultOpen={false}>
          <AppSidebar />
          <main className="p-6">
            {children}
          </main>
        </SidebarProvider>
      </body>
    </html>
  );
}

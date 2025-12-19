import "./globals.css"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import ThemeProvider from "@/components/theme-provider"

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
      <body className="flex min-h-screen">
        <ThemeProvider>
          <SidebarProvider defaultOpen={false}>
            <AppSidebar />
            <main className="flex-1 p-4">{children}</main>
          </SidebarProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}

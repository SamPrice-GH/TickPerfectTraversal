import { FileCode, BadgeDollarSign, History, ChartCandlestick, Plus } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar"
import Link from "next/link"
import ThemeToggle from "@/components/theme-toggle"

const items = [
  {
    title: "Backtest",
    url: "/",
    icon: ChartCandlestick,
  },
  {
    title: "Strategies",
    url: "strategies",
    icon: FileCode,
  },
  {
    title: "Instruments",
    url: "instruments",
    icon: BadgeDollarSign,
  },
  {
    title: "History",
    url: "history",
    icon: History,
  },
]

export function AppSidebar() {
  return (
    <Sidebar collapsible="icon">

      <SidebarContent>

        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild tooltip={item.title}>
                    <Link href={item.url}>
                      <item.icon className="size-5" />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

      </SidebarContent>

      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip={"Toggle theme"}>
              <ThemeToggle />
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  )
}
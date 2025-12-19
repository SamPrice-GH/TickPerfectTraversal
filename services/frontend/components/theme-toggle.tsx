"use client"

import * as React from "react"
import { Sun, Moon } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function ThemeToggle(props: React.ComponentProps<typeof Button>) {
  const [isDark, setIsDark] = React.useState<boolean | null>(null)

  React.useEffect(() => {
    try {
      const stored = localStorage.getItem("theme")
      const prefersDark =
        typeof window !== "undefined" &&
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches

      const effective = stored ? stored === "dark" : prefersDark
      setIsDark(effective)
    } catch (e) {
      setIsDark(false)
    }
  }, [])

  const toggle = React.useCallback(() => {
    try {
      const next = !Boolean(isDark)
      setIsDark(next)
      localStorage.setItem("theme", next ? "dark" : "light")
      document.documentElement.classList.toggle("dark", next)
    } catch (e) {
      // ignore
      alert("theme toggle error: " + e);
    }
  }, [isDark])

  // render placeholder during unknown state
  if (isDark === null) {
    return (
      <Button {...props} variant="ghost" size="icon" aria-label="Toggle theme" disabled>
        <Sun className="size-5 opacity-60" />
      </Button>
    )
  }

  return (
    <Button
      {...props}
      variant={props.variant ?? "ghost"}
      size={props.size ?? "icon"}
      aria-pressed={isDark}
      aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
      onClick={(e) => {
        props.onClick?.(e as any)
        toggle()
      }}
    >
      {isDark ? <Sun className="size-5" /> : <Moon className="size-5" />}
      <span>Switch Theme</span>
    </Button>
  )
}

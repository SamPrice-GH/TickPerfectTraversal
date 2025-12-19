"use client"

import React from "react"

export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  React.useEffect(() => {
    try {
      const stored = localStorage.getItem("theme")
      const prefersDark =
        typeof window !== "undefined" &&
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches

      const isDark = stored ? stored === "dark" : prefersDark

      document.documentElement.classList.toggle("dark", isDark)
    } catch (e) {
      // ignore (e.g. SSR or blocked storage)
      alert("theme provider error: " + e);
    }
  }, [])

  return <>{children}</>
}

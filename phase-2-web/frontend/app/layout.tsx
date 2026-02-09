'use client';

import './globals.css'
import '../app/themes.css'
import { Inter } from 'next/font/google'
import { ThemeProvider } from '@/context/ThemeContext'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Sidebar from '@/components/Sidebar'
import NotificationPrompt from '@/components/NotificationPrompt'
import { useState } from 'react'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  return (
    <html lang="en">
      <head>
        <meta name="theme-color" content="#9333ea" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      </head>
      <body className={inter.className}>
        <ThemeProvider>
          <div className="flex flex-col min-h-screen">
            {/* Header with hamburger menu */}
            <Header userName="User" onMenuClick={toggleSidebar} />

            {/* Main Content Area with Sidebar */}
            <div className="flex flex-1 overflow-hidden">
              {/* Sidebar */}
              <Sidebar isOpen={sidebarOpen} onClose={closeSidebar} />

              {/* Main Content */}
              <main className="flex-1 overflow-y-auto p-4 md:p-6">
                {children}
              </main>
            </div>

            {/* Footer */}
            <Footer />

            {/* Notification Prompt */}
            <NotificationPrompt />
          </div>
        </ThemeProvider>
      </body>
    </html>
  )
}
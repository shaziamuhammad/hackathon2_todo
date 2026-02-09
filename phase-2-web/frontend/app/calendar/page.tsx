'use client'

import { useEffect } from 'react'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'next/navigation'

export default function CalendarPage() {
  const { isAuthenticated, user, logout } = useAuthStore()
  const router = useRouter()

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, router])

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Calendar</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Welcome, {user?.email}</span>
            <button
              onClick={() => router.push('/dashboard')}
              className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-md transition duration-200"
            >
              Dashboard
            </button>
            <button
              onClick={logout}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition duration-200"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="bg-white p-8 rounded-lg shadow text-center">
          <h2 className="text-2xl font-semibold mb-4">Calendar View</h2>
          <p className="text-gray-600">Calendar feature coming soon. View your tasks in the dashboard for now.</p>
          <button
            onClick={() => router.push('/dashboard')}
            className="mt-6 bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-md transition duration-200"
          >
            Go to Dashboard
          </button>
        </div>
      </main>
    </div>
  )
}

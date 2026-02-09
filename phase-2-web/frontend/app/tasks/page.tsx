'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function TasksPage() {
  const router = useRouter()

  useEffect(() => {
    // Redirect to dashboard since tasks are managed there
    router.push('/dashboard')
  }, [router])

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <p className="text-gray-600">Redirecting to dashboard...</p>
      </div>
    </div>
  )
}

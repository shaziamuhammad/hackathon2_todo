'use client'

import { useEffect } from 'react'
import { useAuthStore } from '@/stores/authStore'
import { useTaskStore } from '@/stores/taskStore'
import { TaskInput } from '@/types/task'
import { useRouter } from 'next/navigation'
import TaskList from '@/components/TaskList'
import TaskForm from '@/components/TaskForm'

export default function DashboardPage() {
  const { isAuthenticated, user, logout } = useAuthStore()
  const { tasks, loading, error, fetchTasks } = useTaskStore()
  const router = useRouter()

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    if (user) {
      fetchTasks(user.id)
    }
  }, [isAuthenticated, user, fetchTasks, router])

  const handleAddTask = async (task: TaskInput) => {
    if (user) {
      try {
        await useTaskStore.getState().createTask(user.id, task)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }
  }

  const handleUpdateTask = async (taskId: string, updatedTask: Partial<TaskInput>) => {
    if (user) {
      try {
        await useTaskStore.getState().updateTask(user.id, taskId, updatedTask)
      } catch (err) {
        console.error('Failed to update task:', err)
      }
    }
  }

  const handleDeleteTask = async (taskId: string) => {
    if (user) {
      try {
        await useTaskStore.getState().deleteTask(user.id, taskId)
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }
  }

  const handleToggleComplete = async (taskId: string, completed: boolean) => {
    if (user) {
      try {
        await useTaskStore.getState().toggleTaskCompletion(user.id, taskId)
      } catch (err) {
        console.error('Failed to toggle task completion:', err)
      }
    }
  }

  if (!isAuthenticated) {
    return null // Redirect happens in useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Todo Dashboard</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Welcome, {user?.email}</span>
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
        {/* Stats Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-900">Total Tasks</h3>
            <p className="text-3xl font-bold mt-2">{tasks.length}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-900">Completed</h3>
            <p className="text-3xl font-bold mt-2">{tasks.filter(t => t.completed).length}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-medium text-gray-900">Pending</h3>
            <p className="text-3xl font-bold mt-2">{tasks.filter(t => !t.completed).length}</p>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Task Form */}
          <div className="lg:col-span-1">
            <div className="bg-white p-6 rounded-lg shadow">
              <h2 className="text-xl font-semibold mb-4">Add New Task</h2>
              <TaskForm onSubmit={handleAddTask} loading={loading} />
            </div>
          </div>

          {/* Right Column - Task List */}
          <div className="lg:col-span-2">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold">Your Tasks</h2>
                {loading && <span>Loading...</span>}
                {error && <span className="text-red-500">{error}</span>}
              </div>

              {tasks.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-500">No tasks yet. Add your first task!</p>
                </div>
              ) : (
                <TaskList
                  tasks={tasks}
                  onUpdate={handleUpdateTask}
                  onDelete={handleDeleteTask}
                  onToggleComplete={handleToggleComplete}
                  loading={loading}
                />
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
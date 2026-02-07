import { create } from 'zustand'
import { Task, TaskInput } from '@/types/task'
import api from '@/lib/api'

interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  fetchTasks: (userId: string) => Promise<void>;
  createTask: (userId: string, task: TaskInput) => Promise<void>;
  updateTask: (userId: string, taskId: string, task: Partial<Task>) => Promise<void>;
  deleteTask: (userId: string, taskId: string) => Promise<void>;
  toggleTaskCompletion: (userId: string, taskId: string) => Promise<void>;
}

export const useTaskStore = create<TaskState>((set, get) => ({
  tasks: [],
  loading: false,
  error: null,

  fetchTasks: async (userId) => {
    set({ loading: true, error: null })
    try {
      const response = await api.get(`/tasks/${userId}/tasks`)

      if (response.status !== 200) {
        throw new Error('Failed to fetch tasks')
      }

      const tasks = response.data
      set({ tasks, loading: false })
    } catch (error: any) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  createTask: async (userId, task) => {
    set({ loading: true, error: null })
    try {
      const response = await api.post(`/tasks/${userId}/tasks`, task)

      if (response.status !== 200) {
        throw new Error('Failed to create task')
      }

      const newTask = response.data
      set((state) => ({ tasks: [...state.tasks, newTask], loading: false }))
    } catch (error: any) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  updateTask: async (userId, taskId, updatedTask) => {
    set({ loading: true, error: null })
    try {
      const response = await api.put(`/tasks/${userId}/tasks/${taskId}`, updatedTask)

      if (response.status !== 200) {
        throw new Error('Failed to update task')
      }

      const updatedTaskResult = response.data
      set((state) => ({
        tasks: state.tasks.map(task =>
          task.id === taskId ? updatedTaskResult : task
        ),
        loading: false
      }))
    } catch (error: any) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  deleteTask: async (userId, taskId) => {
    set({ loading: true, error: null })
    try {
      const response = await api.delete(`/tasks/${userId}/tasks/${taskId}`)

      if (response.status !== 200) {
        throw new Error('Failed to delete task')
      }

      set((state) => ({
        tasks: state.tasks.filter(task => task.id !== taskId),
        loading: false
      }))
    } catch (error: any) {
      set({ error: error.message, loading: false })
      throw error
    }
  },

  toggleTaskCompletion: async (userId, taskId) => {
    set({ loading: true, error: null })
    try {
      const response = await api.patch(`/tasks/${userId}/tasks/${taskId}/complete`, { completed: true })

      if (response.status !== 200) {
        throw new Error('Failed to update task completion')
      }

      const updatedTask = response.data
      set((state) => ({
        tasks: state.tasks.map(task =>
          task.id === taskId ? updatedTask : task
        ),
        loading: false
      }))
    } catch (error: any) {
      set({ error: error.message, loading: false })
      throw error
    }
  },
}))
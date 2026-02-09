// phase-2-web\frontend\stores\authStore.ts
import { create } from 'zustand'
import { User } from '@/types/user'
import api from '@/lib/api'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => void
  initializeAuth: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: typeof window !== 'undefined' ? localStorage.getItem('token') : null,
  isAuthenticated: typeof window !== 'undefined' ? !!localStorage.getItem('token') : false,

  login: async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password })

      if (response.status !== 200) {
        throw new Error('Login failed')
      }

      const data = response.data
      const token = data.access_token

      localStorage.setItem('token', token)

      set({
        token,
        isAuthenticated: true,
        user: data.user
      })
    } catch (error: any) {
      console.error('Login error:', error)
      const errorMessage = error.response?.data?.detail || error.message || 'Login failed'
      throw new Error(errorMessage)
    }
  },

  register: async (email, password) => {
    try {
      const response = await api.post('/auth/register', { email, password })

      if (response.status !== 200) {
        throw new Error('Registration failed')
      }

      const data = response.data
      const token = data.access_token

      localStorage.setItem('token', token)

      set({
        token,
        isAuthenticated: true,
        user: data.user
      })
    } catch (error: any) {
      throw new Error(error.message || 'Registration failed')
    }
  },

  logout: () => {
    localStorage.removeItem('token')
    set({ token: null, isAuthenticated: false, user: null })
  },

  initializeAuth: () => {
    const token = localStorage.getItem('token')
    set({
      token: token,
      isAuthenticated: !!token
    })
  },
}))
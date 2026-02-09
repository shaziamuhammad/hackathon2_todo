/**
 * useTaskNotifications Hook
 * Manages task notifications and periodic checking
 */
'use client';

import { useEffect, useState } from 'react';
import notificationService from '@/services/notificationService';
import axios from 'axios';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string;
  priority: string;
  status: string;
}

export function useTaskNotifications() {
  const [isEnabled, setIsEnabled] = useState(false);
  const [tasks, setTasks] = useState<Task[]>([]);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080/api/v1';

  // Fetch tasks from API
  const fetchTasks = async (): Promise<Task[]> => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      if (!token || !userId) {
        return [];
      }

      const response = await axios.get(
        `${API_BASE_URL}/tasks/${userId}/tasks`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      return response.data || [];
    } catch (error) {
      console.error('Error fetching tasks for notifications:', error);
      return [];
    }
  };

  // Initialize notifications
  useEffect(() => {
    const initNotifications = async () => {
      if (notificationService.isSupported()) {
        const enabled = notificationService.isEnabled();
        setIsEnabled(enabled);

        if (enabled) {
          // Fetch tasks immediately
          const fetchedTasks = await fetchTasks();
          setTasks(fetchedTasks);

          // Check for upcoming tasks
          await notificationService.checkUpcomingTasks(fetchedTasks);

          // Start periodic checking (every 15 minutes)
          notificationService.startPeriodicCheck(fetchTasks, 15);
        }
      }
    };

    initNotifications();

    // Cleanup on unmount
    return () => {
      notificationService.stopPeriodicCheck();
    };
  }, []);

  // Request notification permission
  const requestPermission = async (): Promise<boolean> => {
    const granted = await notificationService.requestPermission();
    setIsEnabled(granted);

    if (granted) {
      // Start periodic checking
      const fetchedTasks = await fetchTasks();
      setTasks(fetchedTasks);
      notificationService.startPeriodicCheck(fetchTasks, 15);
    }

    return granted;
  };

  // Notify when a task is created
  const notifyTaskCreated = async (taskTitle: string) => {
    if (isEnabled) {
      await notificationService.notifyTaskCreated(taskTitle);
    }
  };

  // Notify when a task is completed
  const notifyTaskCompleted = async (taskTitle: string) => {
    if (isEnabled) {
      await notificationService.notifyTaskCompleted(taskTitle);
    }
  };

  // Manually trigger a check for upcoming tasks
  const checkNow = async () => {
    if (isEnabled) {
      const fetchedTasks = await fetchTasks();
      setTasks(fetchedTasks);
      await notificationService.checkUpcomingTasks(fetchedTasks);
    }
  };

  return {
    isEnabled,
    isSupported: notificationService.isSupported(),
    permission: notificationService.getPermissionStatus(),
    requestPermission,
    notifyTaskCreated,
    notifyTaskCompleted,
    checkNow,
    tasks,
  };
}

/**
 * useNotifications Hook
 * Manages notification polling and display
 */
'use client';

import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { showTaskDueNotification, showTaskReminderNotification } from '@/lib/notifications';

interface Notification {
  id: string;
  task_id: string;
  title: string;
  message: string;
  notification_type: string;
  scheduled_for: string;
  sent: boolean;
}

interface UseNotificationsReturn {
  notifications: Notification[];
  unreadCount: number;
  isLoading: boolean;
  error: string | null;
  markAsRead: (notificationId: string) => Promise<void>;
  refreshNotifications: () => Promise<void>;
}

export function useNotifications(): UseNotificationsReturn {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const fetchNotifications = useCallback(async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await axios.get(
        `${API_BASE_URL}/api/v1/notifications`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      const fetchedNotifications = response.data.notifications || [];
      setNotifications(fetchedNotifications);
      setUnreadCount(fetchedNotifications.filter((n: Notification) => !n.sent).length);

      // Show browser notifications for new notifications
      for (const notification of fetchedNotifications) {
        if (!notification.sent) {
          if (notification.notification_type === 'due_date') {
            await showTaskDueNotification(
              notification.title,
              new Date(notification.scheduled_for)
            );
          } else {
            await showTaskReminderNotification(notification.title);
          }
        }
      }

      setError(null);
    } catch (err: any) {
      console.error('Error fetching notifications:', err);
      if (err.response?.status !== 401) {
        setError('Failed to fetch notifications');
      }
    }
  }, [API_BASE_URL]);

  const markAsRead = async (notificationId: string) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      await axios.post(
        `${API_BASE_URL}/api/v1/notifications/${notificationId}/mark-sent`,
        {},
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      // Update local state
      setNotifications(prev =>
        prev.map(n =>
          n.id === notificationId ? { ...n, sent: true } : n
        )
      );
      setUnreadCount(prev => Math.max(0, prev - 1));

    } catch (err) {
      console.error('Error marking notification as read:', err);
    }
  };

  const refreshNotifications = async () => {
    setIsLoading(true);
    await fetchNotifications();
    setIsLoading(false);
  };

  // Poll for notifications every 5 minutes
  useEffect(() => {
    fetchNotifications();

    const interval = setInterval(() => {
      fetchNotifications();
    }, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(interval);
  }, [fetchNotifications]);

  // Also check when page becomes visible
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        fetchNotifications();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [fetchNotifications]);

  return {
    notifications,
    unreadCount,
    isLoading,
    error,
    markAsRead,
    refreshNotifications
  };
}

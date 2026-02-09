/**
 * Browser Notifications Manager
 * Handles notification permissions and display
 */

export interface NotificationOptions {
  title: string;
  body: string;
  icon?: string;
  badge?: string;
  tag?: string;
  requireInteraction?: boolean;
  silent?: boolean;
  data?: any;
}

class NotificationManager {
  /**
   * Check if browser supports notifications
   */
  isSupported(): boolean {
    return 'Notification' in window && 'serviceWorker' in navigator;
  }

  /**
   * Get current notification permission status
   */
  getPermissionStatus(): NotificationPermission {
    if (!this.isSupported()) {
      return 'denied';
    }
    return Notification.permission;
  }

  /**
   * Request notification permission from user
   */
  async requestPermission(): Promise<boolean> {
    if (!this.isSupported()) {
      return false;
    }

    try {
      const permission = await Notification.requestPermission();
      return permission === 'granted';
    } catch (error) {
      console.error('Error requesting notification permission:', error);
      return false;
    }
  }

  /**
   * Show a notification
   */
  async showNotification(options: NotificationOptions): Promise<void> {
    if (!this.isSupported()) {
      console.warn('Notifications not supported');
      return;
    }

    if (this.getPermissionStatus() !== 'granted') {
      console.warn('Notification permission not granted');
      return;
    }

    try {
      // If service worker is available, use it for better notification handling
      if ('serviceWorker' in navigator) {
        const registration = await navigator.serviceWorker.ready;
        await registration.showNotification(options.title, {
          body: options.body,
          icon: options.icon || '/favicon.svg',
          badge: options.badge || '/favicon.svg',
          tag: options.tag,
          requireInteraction: options.requireInteraction ?? false,
          silent: options.silent ?? false,
          data: options.data,
        });
      } else {
        // Fallback to basic notification
        new Notification(options.title, {
          body: options.body,
          icon: options.icon || '/favicon.svg',
          tag: options.tag,
          requireInteraction: options.requireInteraction ?? false,
          silent: options.silent ?? false,
          data: options.data,
        });
      }
    } catch (error) {
      console.error('Error showing notification:', error);
    }
  }

  /**
   * Schedule a notification for a specific time
   */
  scheduleNotification(options: NotificationOptions, scheduledTime: Date): void {
    const now = new Date().getTime();
    const scheduledTimeMs = scheduledTime.getTime();
    const delay = scheduledTimeMs - now;

    if (delay <= 0) {
      // Time has already passed, show immediately
      this.showNotification(options);
      return;
    }

    // Schedule for future
    setTimeout(() => {
      this.showNotification(options);
    }, delay);
  }
}

// Export singleton instance
export const notificationManager = new NotificationManager();

// Helper function to show task due notification
export async function showTaskDueNotification(taskTitle: string, dueDate: Date): Promise<void> {
  const timeUntilDue = dueDate.getTime() - Date.now();
  const hoursUntilDue = Math.floor(timeUntilDue / (1000 * 60 * 60));
  const minutesUntilDue = Math.floor((timeUntilDue % (1000 * 60 * 60)) / (1000 * 60));

  let body = '';
  if (hoursUntilDue > 0) {
    body = `Due in ${hoursUntilDue} hour${hoursUntilDue > 1 ? 's' : ''}`;
  } else if (minutesUntilDue > 0) {
    body = `Due in ${minutesUntilDue} minute${minutesUntilDue > 1 ? 's' : ''}`;
  } else {
    body = 'Due now!';
  }

  await notificationManager.showNotification({
    title: `Task Due: ${taskTitle}`,
    body: body,
    tag: `task-due-${taskTitle}`,
    requireInteraction: true
  });
}

// Helper function to show task reminder notification
export async function showTaskReminderNotification(taskTitle: string): Promise<void> {
  await notificationManager.showNotification({
    title: 'Task Reminder',
    body: `Don't forget: ${taskTitle}`,
    tag: `task-reminder-${taskTitle}`,
    requireInteraction: false
  });
}

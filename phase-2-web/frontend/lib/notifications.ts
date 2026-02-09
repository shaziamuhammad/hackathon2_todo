/**
 * Browser Notification Utilities
 * Handles browser notification API integration
 */

export interface NotificationOptions {
  title: string;
  body: string;
  icon?: string;
  tag?: string;
  requireInteraction?: boolean;
}

class NotificationManager {
  private permission: NotificationPermission = 'default';

  constructor() {
    if (typeof window !== 'undefined' && 'Notification' in window) {
      this.permission = Notification.permission;
    }
  }

  /**
   * Request permission to show notifications
   */
  async requestPermission(): Promise<boolean> {
    if (!('Notification' in window)) {
      console.warn('This browser does not support notifications');
      return false;
    }

    if (this.permission === 'granted') {
      return true;
    }

    try {
      const permission = await Notification.requestPermission();
      this.permission = permission;
      return permission === 'granted';
    } catch (error) {
      console.error('Error requesting notification permission:', error);
      return false;
    }
  }

  /**
   * Show a browser notification
   */
  async showNotification(options: NotificationOptions): Promise<boolean> {
    if (!('Notification' in window)) {
      console.warn('This browser does not support notifications');
      return false;
    }

    // Request permission if not already granted
    if (this.permission !== 'granted') {
      const granted = await this.requestPermission();
      if (!granted) {
        return false;
      }
    }

    try {
      const notification = new Notification(options.title, {
        body: options.body,
        icon: options.icon || '/icon-192x192.png',
        tag: options.tag,
        requireInteraction: options.requireInteraction || false,
        badge: '/icon-96x96.png'
      });

      // Auto-close after 5 seconds if not requiring interaction
      if (!options.requireInteraction) {
        setTimeout(() => notification.close(), 5000);
      }

      // Handle notification click
      notification.onclick = () => {
        window.focus();
        notification.close();
      };

      return true;
    } catch (error) {
      console.error('Error showing notification:', error);
      return false;
    }
  }

  /**
   * Check if notifications are supported and permitted
   */
  isSupported(): boolean {
    return typeof window !== 'undefined' && 'Notification' in window;
  }

  /**
   * Check if permission is granted
   */
  isPermissionGranted(): boolean {
    return this.permission === 'granted';
  }

  /**
   * Get current permission status
   */
  getPermissionStatus(): NotificationPermission {
    return this.permission;
  }
}

// Create singleton instance
export const notificationManager = new NotificationManager();

// Helper function to show task due notification
export async function showTaskDueNotification(taskTitle: string, dueDate: Date): Promise<boolean> {
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

  return notificationManager.showNotification({
    title: `Task Due: ${taskTitle}`,
    body: body,
    tag: `task-due-${taskTitle}`,
    requireInteraction: true
  });
}

// Helper function to show task reminder notification
export async function showTaskReminderNotification(taskTitle: string): Promise<boolean> {
  return notificationManager.showNotification({
    title: 'Task Reminder',
    body: `Don't forget: ${taskTitle}`,
    tag: `task-reminder-${taskTitle}`,
    requireInteraction: false
  });
}

/**
 * Browser Notification Service
 * Handles browser notifications for task reminders and due dates
 */

export interface NotificationOptions {
  title: string;
  body: string;
  icon?: string;
  tag?: string;
  requireInteraction?: boolean;
}

class NotificationService {
  private permission: NotificationPermission = 'default';
  private checkInterval: NodeJS.Timeout | null = null;

  constructor() {
    if (typeof window !== 'undefined' && 'Notification' in window) {
      this.permission = Notification.permission;
    }
  }

  /**
   * Request notification permission from the user
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
   * Check if notifications are supported and permitted
   */
  isSupported(): boolean {
    return typeof window !== 'undefined' && 'Notification' in window;
  }

  /**
   * Check if notifications are enabled
   */
  isEnabled(): boolean {
    return this.isSupported() && this.permission === 'granted';
  }

  /**
   * Show a browser notification
   */
  async show(options: NotificationOptions): Promise<void> {
    if (!this.isEnabled()) {
      console.warn('Notifications are not enabled');
      return;
    }

    try {
      const notification = new Notification(options.title, {
        body: options.body,
        icon: options.icon || '/favicon.ico',
        tag: options.tag,
        requireInteraction: options.requireInteraction || false,
        badge: '/favicon.ico',
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
    } catch (error) {
      console.error('Error showing notification:', error);
    }
  }

  /**
   * Show a task due notification
   */
  async notifyTaskDue(taskTitle: string, dueDate: Date): Promise<void> {
    const now = new Date();
    const timeUntilDue = dueDate.getTime() - now.getTime();
    const hoursUntilDue = Math.floor(timeUntilDue / (1000 * 60 * 60));
    const minutesUntilDue = Math.floor(timeUntilDue / (1000 * 60));

    let body = '';
    if (timeUntilDue < 0) {
      body = `Task "${taskTitle}" is overdue!`;
    } else if (hoursUntilDue < 1) {
      body = `Task "${taskTitle}" is due in ${minutesUntilDue} minutes`;
    } else if (hoursUntilDue < 24) {
      body = `Task "${taskTitle}" is due in ${hoursUntilDue} hours`;
    } else {
      const daysUntilDue = Math.floor(hoursUntilDue / 24);
      body = `Task "${taskTitle}" is due in ${daysUntilDue} days`;
    }

    await this.show({
      title: '📋 Task Reminder',
      body,
      tag: `task-due-${taskTitle}`,
      requireInteraction: timeUntilDue < 0, // Require interaction for overdue tasks
    });
  }

  /**
   * Show a task completion notification
   */
  async notifyTaskCompleted(taskTitle: string): Promise<void> {
    await this.show({
      title: '✅ Task Completed',
      body: `Great job! You completed "${taskTitle}"`,
      tag: `task-completed-${taskTitle}`,
    });
  }

  /**
   * Show a task created notification
   */
  async notifyTaskCreated(taskTitle: string): Promise<void> {
    await this.show({
      title: '➕ Task Created',
      body: `New task added: "${taskTitle}"`,
      tag: `task-created-${taskTitle}`,
    });
  }

  /**
   * Check for upcoming task due dates and send notifications
   */
  async checkUpcomingTasks(tasks: any[]): Promise<void> {
    if (!this.isEnabled()) {
      return;
    }

    const now = new Date();
    const oneDayFromNow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
    const oneHourFromNow = new Date(now.getTime() + 60 * 60 * 1000);

    for (const task of tasks) {
      if (!task.due_date || task.completed) {
        continue;
      }

      const dueDate = new Date(task.due_date);

      // Notify for overdue tasks
      if (dueDate < now) {
        await this.notifyTaskDue(task.title, dueDate);
      }
      // Notify for tasks due within 1 hour
      else if (dueDate < oneHourFromNow) {
        await this.notifyTaskDue(task.title, dueDate);
      }
      // Notify for tasks due within 24 hours (once per day)
      else if (dueDate < oneDayFromNow) {
        const lastNotified = localStorage.getItem(`notified-${task.id}`);
        const lastNotifiedDate = lastNotified ? new Date(lastNotified) : null;

        // Only notify once per day
        if (!lastNotifiedDate || now.getTime() - lastNotifiedDate.getTime() > 24 * 60 * 60 * 1000) {
          await this.notifyTaskDue(task.title, dueDate);
          localStorage.setItem(`notified-${task.id}`, now.toISOString());
        }
      }
    }
  }

  /**
   * Start periodic checking for upcoming tasks
   */
  startPeriodicCheck(fetchTasks: () => Promise<any[]>, intervalMinutes: number = 15): void {
    if (this.checkInterval) {
      this.stopPeriodicCheck();
    }

    // Check immediately
    fetchTasks().then(tasks => this.checkUpcomingTasks(tasks));

    // Then check periodically
    this.checkInterval = setInterval(async () => {
      const tasks = await fetchTasks();
      await this.checkUpcomingTasks(tasks);
    }, intervalMinutes * 60 * 1000);
  }

  /**
   * Stop periodic checking
   */
  stopPeriodicCheck(): void {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = null;
    }
  }

  /**
   * Get notification permission status
   */
  getPermissionStatus(): NotificationPermission {
    return this.permission;
  }
}

// Export singleton instance
const notificationService = new NotificationService();
export default notificationService;

/**
 * NotificationSettings Component
 * Allows users to enable/disable browser notifications
 */
'use client';

import React, { useState, useEffect } from 'react';
import notificationService from '@/services/notificationService';

export default function NotificationSettings() {
  const [isSupported, setIsSupported] = useState(false);
  const [permission, setPermission] = useState<NotificationPermission>('default');
  const [isEnabled, setIsEnabled] = useState(false);

  useEffect(() => {
    // Check if notifications are supported
    setIsSupported(notificationService.isSupported());
    setPermission(notificationService.getPermissionStatus());
    setIsEnabled(notificationService.isEnabled());
  }, []);

  const handleEnableNotifications = async () => {
    const granted = await notificationService.requestPermission();
    if (granted) {
      setPermission('granted');
      setIsEnabled(true);

      // Show a test notification
      await notificationService.show({
        title: '🔔 Notifications Enabled',
        body: 'You will now receive task reminders and due date notifications',
      });
    } else {
      setPermission(notificationService.getPermissionStatus());
      setIsEnabled(false);
    }
  };

  if (!isSupported) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div className="flex items-start">
          <svg className="h-5 w-5 text-yellow-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-yellow-800">
              Notifications Not Supported
            </h3>
            <p className="mt-1 text-sm text-yellow-700">
              Your browser does not support notifications. Please use a modern browser like Chrome, Firefox, or Safari.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-4 md:p-6">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Browser Notifications
          </h3>
          <p className="text-sm text-gray-600 mb-4">
            Get notified about upcoming task due dates and reminders
          </p>

          {/* Permission Status */}
          <div className="flex items-center space-x-2 mb-4">
            <span className="text-sm font-medium text-gray-700">Status:</span>
            {permission === 'granted' && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                <svg className="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Enabled
              </span>
            )}
            {permission === 'denied' && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                <svg className="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                Blocked
              </span>
            )}
            {permission === 'default' && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                <svg className="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
                Not Set
              </span>
            )}
          </div>

          {/* Enable Button */}
          {!isEnabled && permission !== 'denied' && (
            <button
              onClick={handleEnableNotifications}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium"
            >
              Enable Notifications
            </button>
          )}

          {/* Blocked Message */}
          {permission === 'denied' && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3 mt-2">
              <p className="text-sm text-red-800">
                Notifications are blocked. To enable them, please update your browser settings:
              </p>
              <ul className="mt-2 text-xs text-red-700 list-disc list-inside space-y-1">
                <li>Click the lock icon in the address bar</li>
                <li>Find "Notifications" in the permissions list</li>
                <li>Change the setting to "Allow"</li>
                <li>Refresh this page</li>
              </ul>
            </div>
          )}

          {/* Enabled Message */}
          {isEnabled && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-3 mt-2">
              <p className="text-sm text-green-800">
                ✓ You'll receive notifications for:
              </p>
              <ul className="mt-2 text-xs text-green-700 list-disc list-inside space-y-1">
                <li>Tasks due within 24 hours</li>
                <li>Tasks due within 1 hour</li>
                <li>Overdue tasks</li>
                <li>Task completions</li>
              </ul>
            </div>
          )}
        </div>

        {/* Notification Icon */}
        <div className="ml-4">
          <svg
            className={`h-12 w-12 ${isEnabled ? 'text-purple-600' : 'text-gray-400'}`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
            />
          </svg>
        </div>
      </div>
    </div>
  );
}

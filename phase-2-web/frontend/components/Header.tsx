/**
 * Header Component
 * Navigation and user profile
 */
'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import ThemeToggle from './ThemeToggle';

interface HeaderProps {
  userName?: string;
  onLogout?: () => void;
  onMenuClick?: () => void;
}

export default function Header({ userName, onLogout, onMenuClick }: HeaderProps) {
  const [showUserMenu, setShowUserMenu] = useState(false);

  return (
    <header className="bg-purple-600 text-white shadow-md sticky top-0 z-30">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-14 md:h-16">
          {/* Hamburger Menu Button (Mobile) */}
          <button
            onClick={onMenuClick}
            className="md:hidden p-2 rounded-md hover:bg-purple-700 transition-colors"
            aria-label="Toggle menu"
          >
            <svg
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>

          {/* Logo and Brand */}
          <div className="flex items-center space-x-2 md:space-x-4">
            <Link href="/" className="flex items-center space-x-2">
              <svg
                className="h-6 w-6 md:h-8 md:w-8"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
                />
              </svg>
              <span className="text-lg md:text-xl font-bold">AI Todo</span>
            </Link>
          </div>

          {/* Navigation (Desktop) */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link
              href="/tasks"
              className="hover:text-purple-200 transition-colors text-sm lg:text-base"
            >
              My Tasks
            </Link>
            <Link
              href="/chat"
              className="hover:text-purple-200 transition-colors text-sm lg:text-base"
            >
              AI Assistant
            </Link>
            <Link
              href="/calendar"
              className="hover:text-purple-200 transition-colors text-sm lg:text-base"
            >
              Calendar
            </Link>
          </nav>

          {/* Theme Toggle and User Menu */}
          <div className="flex items-center space-x-2 md:space-x-4">
            {/* Theme Toggle */}
            <div className="hidden sm:block">
              <ThemeToggle />
            </div>

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-1 md:space-x-2 hover:text-purple-200 transition-colors"
              >
                <div className="h-8 w-8 rounded-full bg-purple-700 flex items-center justify-center">
                  <span className="text-sm font-semibold">
                    {userName ? userName.charAt(0).toUpperCase() : 'U'}
                  </span>
                </div>
                <span className="hidden lg:inline text-sm">{userName || 'User'}</span>
                <svg
                  className="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>

              {/* Dropdown Menu */}
              {showUserMenu && (
                <>
                  {/* Backdrop for mobile */}
                  <div
                    className="fixed inset-0 z-40 md:hidden"
                    onClick={() => setShowUserMenu(false)}
                  />

                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                    <Link
                      href="/profile"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      onClick={() => setShowUserMenu(false)}
                    >
                      Profile Settings
                    </Link>
                    <Link
                      href="/preferences"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      onClick={() => setShowUserMenu(false)}
                    >
                      Preferences
                    </Link>
                    {/* Theme toggle for mobile */}
                    <div className="sm:hidden px-4 py-2 border-t border-gray-200">
                      <span className="text-xs text-gray-500 mb-2 block">Theme</span>
                      <ThemeToggle />
                    </div>
                    <hr className="my-1" />
                    <button
                      onClick={() => {
                        setShowUserMenu(false);
                        onLogout?.();
                      }}
                      className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                    >
                      Logout
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="md:hidden border-t border-purple-700">
        <nav className="flex justify-around py-2">
          <Link
            href="/tasks"
            className="text-xs sm:text-sm hover:text-purple-200 transition-colors px-2 py-1"
          >
            Tasks
          </Link>
          <Link
            href="/chat"
            className="text-xs sm:text-sm hover:text-purple-200 transition-colors px-2 py-1"
          >
            Chat
          </Link>
          <Link
            href="/calendar"
            className="text-xs sm:text-sm hover:text-purple-200 transition-colors px-2 py-1"
          >
            Calendar
          </Link>
        </nav>
      </div>
    </header>
  );
}

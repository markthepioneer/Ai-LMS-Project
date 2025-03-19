import React, { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useTheme } from '../hooks/useTheme';
import {
  Bars3Icon,
  XMarkIcon,
  HomeIcon,
  CurrencyDollarIcon,
  HeartIcon,
  ClipboardDocumentCheckIcon,
  ChartPieIcon,
  BellAlertIcon,
  EnvelopeIcon,
  ScaleIcon,
  UserIcon,
  Cog6ToothIcon,
  SunIcon,
  MoonIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/react/24/outline';

// Navigation items for the sidebar
const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  {
    name: 'Finance',
    href: '/finance',
    icon: CurrencyDollarIcon,
    children: [
      { name: 'Overview', href: '/finance' },
      { name: 'Transactions', href: '/finance/transactions' },
      { name: 'Budgets', href: '/finance/budgets' },
      { name: 'Insights', href: '/finance/insights' }
    ]
  },
  {
    name: 'Health',
    href: '/health',
    icon: HeartIcon,
    children: [
      { name: 'Overview', href: '/health' },
      { name: 'Sleep', href: '/health/sleep' },
      { name: 'Exercise', href: '/health/exercise' },
      { name: 'Insights', href: '/health/insights' }
    ]
  },
  {
    name: 'Tasks',
    href: '/tasks',
    icon: ClipboardDocumentCheckIcon,
    children: [
      { name: 'Overview', href: '/tasks' },
      { name: 'Calendar', href: '/tasks/calendar' },
      { name: 'Analytics', href: '/tasks/analytics' }
    ]
  },
  {
    name: 'Portfolio',
    href: '/portfolio',
    icon: ChartPieIcon,
    children: [
      { name: 'Overview', href: '/portfolio' },
      { name: 'Investments', href: '/portfolio/investments' },
      { name: 'Analytics', href: '/portfolio/analytics' }
    ]
  },
  {
    name: 'Memory',
    href: '/memory',
    icon: BellAlertIcon,
    children: [
      { name: 'Overview', href: '/memory' },
      { name: 'Contacts', href: '/memory/contacts' },
      { name: 'Reminders', href: '/memory/reminders' },
      { name: 'Events', href: '/memory/events' }
    ]
  },
  {
    name: 'Email',
    href: '/email',
    icon: EnvelopeIcon,
    children: [
      { name: 'Overview', href: '/email' },
      { name: 'Inbox', href: '/email/inbox' },
      { name: 'Templates', href: '/email/templates' },
      { name: 'Analytics', href: '/email/analytics' }
    ]
  },
  {
    name: 'Life Balance',
    href: '/life-balance',
    icon: ScaleIcon,
    children: [
      { name: 'Overview', href: '/life-balance' },
      { name: 'Goals', href: '/life-balance/goals' },
      { name: 'Analytics', href: '/life-balance/analytics' }
    ]
  }
];

const userNavigation = [
  { name: 'Your Profile', href: '/profile', icon: UserIcon },
  { name: 'Settings', href: '/settings', icon: Cog6ToothIcon }
];

const DashboardLayout: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [openMenus, setOpenMenus] = useState<Record<string, boolean>>({});

  // Check if a route is active
  const isActive = (href: string) => {
    return location.pathname === href || location.pathname.startsWith(`${href}/`);
  };

  // Toggle submenu visibility
  const toggleMenu = (name: string) => {
    setOpenMenus(prev => ({
      ...prev,
      [name]: !prev[name]
    }));
  };

  // Handle logout
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-40 flex md:hidden ${sidebarOpen ? '' : 'hidden'}`} role="dialog" aria-modal="true">
        {/* Overlay */}
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />

        {/* Sidebar */}
        <div className="relative flex flex-col flex-1 w-full max-w-xs pt-5 pb-4 bg-white dark:bg-gray-800">
          {/* Close button */}
          <div className="absolute top-0 right-0 pt-2 pr-2">
            <button
              type="button"
              className="flex items-center justify-center p-2 text-gray-400 rounded-md hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700"
              onClick={() => setSidebarOpen(false)}
            >
              <span className="sr-only">Close menu</span>
              <XMarkIcon className="w-6 h-6" aria-hidden="true" />
            </button>
          </div>

          {/* Logo */}
          <div className="flex items-center flex-shrink-0 px-4">
            <span className="text-xl font-semibold text-primary-600 dark:text-primary-500">Ai-LMS</span>
          </div>

          {/* Navigation */}
          <div className="flex flex-col flex-1 h-0 mt-5 overflow-y-auto">
            <nav className="flex-1 px-2 space-y-1">
              {navigation.map((item) => (
                <div key={item.name}>
                  {item.children ? (
                    <>
                      <button
                        onClick={() => toggleMenu(item.name)}
                        className={`${
                          isActive(item.href)
                            ? 'bg-primary-100 text-primary-900 dark:bg-primary-900 dark:text-primary-100'
                            : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                        } group w-full flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                      >
                        <item.icon
                          className={`${
                            isActive(item.href) ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-300'
                          } mr-3 flex-shrink-0 h-6 w-6`}
                          aria-hidden="true"
                        />
                        {item.name}
                        <svg
                          className={`${
                            openMenus[item.name] ? 'transform rotate-90' : ''
                          } ml-auto h-5 w-5 transition-transform`}
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 20 20"
                          fill="currentColor"
                          aria-hidden="true"
                        >
                          <path
                            fillRule="evenodd"
                            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                            clipRule="evenodd"
                          />
                        </svg>
                      </button>

                      {openMenus[item.name] && (
                        <div className="pl-8 space-y-1">
                          {item.children.map((subItem) => (
                            <Link
                              key={subItem.name}
                              to={subItem.href}
                              className={`${
                                isActive(subItem.href)
                                  ? 'bg-primary-50 text-primary-700 dark:bg-primary-900 dark:text-primary-100'
                                  : 'text-gray-600 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-700'
                              } group flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                              onClick={() => setSidebarOpen(false)}
                            >
                              {subItem.name}
                            </Link>
                          ))}
                        </div>
                      )}
                    </>
                  ) : (
                    <Link
                      to={item.href}
                      className={`${
                        isActive(item.href)
                          ? 'bg-primary-100 text-primary-900 dark:bg-primary-900 dark:text-primary-100'
                          : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                      } group flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                      onClick={() => setSidebarOpen(false)}
                    >
                      <item.icon
                        className={`${
                          isActive(item.href) ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-300'
                        } mr-3 flex-shrink-0 h-6 w-6`}
                        aria-hidden="true"
                      />
                      {item.name}
                    </Link>
                  )}
                </div>
              ))}
            </nav>
          </div>
        </div>
      </div>

      {/* Static sidebar for desktop */}
      <div className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
        <div className="flex flex-col flex-1 min-h-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
          <div className="flex items-center h-16 flex-shrink-0 px-4 border-b border-gray-200 dark:border-gray-700">
            <span className="text-xl font-semibold text-primary-600 dark:text-primary-500">Ai-LMS</span>
          </div>
          <div className="flex flex-col flex-1 pt-5 pb-4 overflow-y-auto">
            <nav className="flex-1 px-2 space-y-1">
              {navigation.map((item) => (
                <div key={item.name}>
                  {item.children ? (
                    <>
                      <button
                        onClick={() => toggleMenu(item.name)}
                        className={`${
                          isActive(item.href)
                            ? 'bg-primary-100 text-primary-900 dark:bg-primary-900 dark:text-primary-100'
                            : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                        } group w-full flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                      >
                        <item.icon
                          className={`${
                            isActive(item.href) ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-300'
                          } mr-3 flex-shrink-0 h-6 w-6`}
                          aria-hidden="true"
                        />
                        {item.name}
                        <svg
                          className={`${
                            openMenus[item.name] ? 'transform rotate-90' : ''
                          } ml-auto h-5 w-5 transition-transform`}
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 20 20"
                          fill="currentColor"
                          aria-hidden="true"
                        >
                          <path
                            fillRule="evenodd"
                            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                            clipRule="evenodd"
                          />
                        </svg>
                      </button>

                      {openMenus[item.name] && (
                        <div className="pl-8 space-y-1">
                          {item.children.map((subItem) => (
                            <Link
                              key={subItem.name}
                              to={subItem.href}
                              className={`${
                                isActive(subItem.href)
                                  ? 'bg-primary-50 text-primary-700 dark:bg-primary-900 dark:text-primary-100'
                                  : 'text-gray-600 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-700'
                              } group flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                            >
                              {subItem.name}
                            </Link>
                          ))}
                        </div>
                      )}
                    </>
                  ) : (
                    <Link
                      to={item.href}
                      className={`${
                        isActive(item.href)
                          ? 'bg-primary-100 text-primary-900 dark:bg-primary-900 dark:text-primary-100'
                          : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                      } group flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                    >
                      <item.icon
                        className={`${
                          isActive(item.href) ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-300'
                        } mr-3 flex-shrink-0 h-6 w-6`}
                        aria-hidden="true"
                      />
                      {item.name}
                    </Link>
                  )}
                </div>
              ))}
            </nav>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="md:pl-64 flex flex-col min-h-screen">
        {/* Top header */}
        <div className="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white dark:bg-gray-800 shadow border-b border-gray-200 dark:border-gray-700">
          <button
            type="button"
            className="px-4 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 md:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <span className="sr-only">Open sidebar</span>
            <Bars3Icon className="h-6 w-6" aria-hidden="true" />
          </button>
          
          {/* Header content */}
          <div className="flex-1 px-4 flex justify-between">
            <div className="flex-1 flex items-center">
              {/* Page title would go here */}
            </div>
            <div className="ml-4 flex items-center md:ml-6 space-x-4">
              {/* Theme toggle */}
              <button
                onClick={toggleTheme}
                className="p-1 rounded-full text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                {theme === 'dark' ? (
                  <SunIcon className="h-6 w-6" aria-hidden="true" />
                ) : (
                  <MoonIcon className="h-6 w-6" aria-hidden="true" />
                )}
              </button>

              {/* Profile dropdown */}
              <div className="relative">
                <div className="flex items-center">
                  <div className="flex items-center">
                    <span className="hidden md:block mr-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                      {user?.name || 'User'}
                    </span>
                    <div className="h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center text-white">
                      {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
                    </div>
                  </div>
                </div>
              </div>

              {/* User navigation */}
              <div className="hidden md:flex items-center space-x-2">
                {userNavigation.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
                  >
                    <item.icon className="h-6 w-6" aria-hidden="true" />
                  </Link>
                ))}
                
                {/* Logout button */}
                <button
                  onClick={handleLogout}
                  className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
                >
                  <ArrowRightOnRectangleIcon className="h-6 w-6" aria-hidden="true" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Main content area */}
        <main className="flex-1">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              <Outlet />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;

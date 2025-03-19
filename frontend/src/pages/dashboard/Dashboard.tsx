import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import {
  CurrencyDollarIcon,
  HeartIcon,
  ClipboardDocumentCheckIcon,
  ChartPieIcon,
  BellAlertIcon,
  EnvelopeIcon,
  ScaleIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  ClockIcon,
  ExclamationCircleIcon,
} from '@heroicons/react/24/outline';

// Example summary data for modules
// In a real app, this would come from API calls
const dashboardSummary = {
  finance: {
    balance: 12450.78,
    income: 5680.25,
    expenses: 3245.67,
    trend: 'up',
    trendPercentage: 12.5,
    alerts: [
      { id: 1, message: 'Monthly budget for dining out exceeded', severity: 'warning' }
    ]
  },
  health: {
    sleepScore: 87,
    exerciseMinutes: 145,
    weeklyGoal: 150,
    trend: 'up',
    trendPercentage: 5.2,
    alerts: []
  },
  tasks: {
    completed: 12,
    inProgress: 5,
    upcoming: 8,
    overdue: 2,
    trend: 'down',
    trendPercentage: 8.3,
    alerts: [
      { id: 1, message: '2 tasks are overdue', severity: 'error' }
    ]
  },
  portfolio: {
    value: 87450.34,
    gain: 1240.56,
    gainPercentage: 1.45,
    trend: 'up',
    trendPercentage: 1.45,
    alerts: []
  },
  memory: {
    upcomingEvents: 3,
    upcomingBirthdays: 1,
    reminders: 4,
    trend: 'neutral',
    trendPercentage: 0,
    alerts: [
      { id: 1, message: 'Jane Smith\'s birthday is tomorrow', severity: 'info' }
    ]
  },
  email: {
    unread: 8,
    important: 3,
    drafts: 2,
    trend: 'up',
    trendPercentage: 15.8,
    alerts: []
  },
  lifeBalance: {
    score: 7.8,
    maxScore: 10,
    areas: [
      { name: 'Work', score: 6 },
      { name: 'Health', score: 8 },
      { name: 'Relationships', score: 9 },
      { name: 'Personal Growth', score: 7 },
      { name: 'Recreation', score: 8 },
    ],
    trend: 'up',
    trendPercentage: 3.2,
    alerts: []
  }
};

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const currentTime = new Date();
  const hour = currentTime.getHours();
  
  // Determine greeting based on time of day
  let greeting = '';
  if (hour < 12) greeting = 'Good morning';
  else if (hour < 18) greeting = 'Good afternoon';
  else greeting = 'Good evening';

  // Count total alerts
  const totalAlerts = Object.values(dashboardSummary).reduce(
    (count, module) => count + module.alerts.length, 
    0
  );

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          {greeting}, {user?.name || 'User'}
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Here's what's happening across your life today.
        </p>
      </div>

      {/* Alerts summary */}
      {totalAlerts > 0 && (
        <div className="mb-6 bg-white dark:bg-gray-800 rounded-lg shadow-card p-4">
          <h2 className="text-lg font-medium text-gray-900 dark:text-white flex items-center mb-2">
            <ExclamationCircleIcon className="h-5 w-5 mr-2 text-warning-500" />
            Alerts ({totalAlerts})
          </h2>
          <div className="space-y-2">
            {Object.entries(dashboardSummary).map(([moduleKey, moduleData]) => 
              moduleData.alerts.map(alert => (
                <div 
                  key={`${moduleKey}-${alert.id}`} 
                  className={`p-3 rounded-md ${
                    alert.severity === 'error' 
                      ? 'bg-danger-50 text-danger-800 dark:bg-danger-900 dark:text-danger-200' 
                      : alert.severity === 'warning'
                      ? 'bg-warning-50 text-warning-800 dark:bg-warning-900 dark:text-warning-200'
                      : 'bg-primary-50 text-primary-800 dark:bg-primary-900 dark:text-primary-200'
                  }`}
                >
                  <div className="flex">
                    <div className="flex-1">
                      <p className="text-sm font-medium">
                        {moduleKey.charAt(0).toUpperCase() + moduleKey.slice(1)}: {alert.message}
                      </p>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Module Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Finance Module */}
        <Link to="/finance" className="card hover:ring-2 hover:ring-primary-500 transition-all">
          <div className="p-6">
            <div className="flex items-center mb-4">
              <div className="bg-primary-100 dark:bg-primary-900 p-3 rounded-lg">
                <CurrencyDollarIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
              </div>
              <h2 className="ml-3 text-xl font-semibold text-gray-900 dark:text-white">Finance</h2>
            </div>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Balance</span>
                <span className="text-lg font-medium text-gray-900 dark:text-white">
                  ${dashboardSummary.finance.balance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Income</span>
                <span className="text-success-600 dark:text-success-400">
                  +${dashboardSummary.finance.income.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Expenses</span>
                <span className="text-danger-600 dark:text-danger-400">
                  -${dashboardSummary.finance.expenses.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </span>
              </div>
              {dashboardSummary.finance.trend === 'up' ? (
                <div className="flex items-center text-success-600 dark:text-success-400">
                  <ArrowTrendingUpIcon className="h-5 w-5 mr-1" />
                  <span>{dashboardSummary.finance.trendPercentage}% from last month</span>
                </div>
              ) : (
                <div className="flex items-center text-danger-600 dark:text-danger-400">
                  <ArrowTrendingDownIcon className="h-5 w-5 mr-1" />
                  <span>{dashboardSummary.finance.trendPercentage}% from last month</span>
                </div>
              )}
            </div>
          </div>
        </Link>

        {/* Health Module */}
        <Link to="/health" className="card hover:ring-2 hover:ring-primary-500 transition-all">
          <div className="p-6">
            <div className="flex items-center mb-4">
              <div className="bg-success-100 dark:bg-success-900 p-3 rounded-lg">
                <HeartIcon className="h-6 w-6 text-success-600 dark:text-success-400" />
              </div>
              <h2 className="ml-3 text-xl font-semibold text-gray-900 dark:text-white">Health</h2>
            </div>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Sleep Score</span>
                <span className="text-lg font-medium text-gray-900 dark:text-white">
                  {dashboardSummary.health.sleepScore}/100
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Exercise</span>
                <span className="text-lg font-medium text-gray-900 dark:text-white">
                  {dashboardSummary.health.exerciseMinutes} min / {dashboardSummary.health.weeklyGoal} min
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                <div
                  className="bg-success-600 h-2.5 rounded-full"
                  style={{ width: `${Math.min(100, (dashboardSummary.health.exerciseMinutes / dashboardSummary.health.weeklyGoal) * 100)}%` }}
                ></div>
              </div>
              {dashboardSummary.health.trend === 'up' ? (
                <div className="flex items-center text-success-600 dark:text-success-400">
                  <ArrowTrendingUpIcon className="h-5 w-5 mr-1" />
                  <span>{dashboardSummary.health.trendPercentage}% improvement</span>
                </div>
              ) : (
                <div className="flex items-center text-danger-600 dark:text-danger-400">
                  <ArrowTrendingDownIcon className="h-5 w-5 mr-1" />
                  <span>{dashboardSummary.health.trendPercentage}% decrease</span>
                </div>
              )}
            </div>
          </div>
        </Link>

        {/* Tasks Module */}
        <Link to="/tasks" className="card hover:ring-2 hover:ring-primary-500 transition-all">
          <div className="p-6">
            <div className="flex items-center mb-4">
              <div className="bg-secondary-100 dark:bg-secondary-900 p-3 rounded-lg">
                <ClipboardDocumentCheckIcon className="h-6 w-6 text-secondary-600 dark:text-secondary-400" />
              </div>
              <h2 className="ml-3 text-xl font-semibold text-gray-900 dark:text-white">Tasks</h2>
            </div>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-2">
                <div className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="text-gray-500 dark:text-gray-400 text-sm">Completed</p>
                  <p className="text-xl font-medium text-gray-900 dark:text-white">{dashboardSummary.tasks.completed}</p>
                </div>
                <div className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="text-gray-500 dark:text-gray-400 text-sm">In Progress</p>
                  <p className="text-xl font-medium text-gray-900 dark:text-white">{dashboardSummary.tasks.inProgress}</p>
                </div>
                <div className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="text-gray-500 dark:text-gray-400 text-sm">Upcoming</p>
                  <p className="text-xl font-medium text-gray-900 dark:text-white">{dashboardSummary.tasks.upcoming}</p>
                </div>
                <div className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="text-gray-500 dark:text-gray-400 text-sm">Overdue</p>
                  <p className="text-xl font-medium text-danger-600 dark:text-danger-400">{dashboardSummary.tasks.overdue}</p>
                </div>
              </div>
              {dashboardSummary.tasks.trend === 'up' ? (
                <div className="flex items-center text-success-600 dark:text-success-400">
                  <ArrowTrendingUpIcon className="h-5 w-5 mr-1" />
                  <span>{dashboardSummary.tasks.trendPercentage}% more completed</span>
                </div>
              ) : (
                <div className="flex items-center text-danger-600 dark:text-danger-400">
                  <ArrowTrendingDownIcon className="h-5 w-5 mr-1" />
                  <span>{dashboardSummary.tasks.trendPercentage}% fewer completed</span>
                </div>
              )}
            </div>
          </div>
        </Link>

        {/* Portfolio Module */}
        <Link to="/portfolio" className="card hover:ring-2 hover:ring-primary-500 transition-all">
          <div className="p-6">
            <div className="flex items-center mb-4">
              <div className="bg-warning-100 dark:bg-warning-900 p-3 rounded-lg">
                <ChartPieIcon className="h-6 w-6 text-warning-600 dark:text-warning-400" />
              </div>
              <h2 className="ml-3 text-xl font-semibold text-gray-900 dark:text-white">Portfolio</h2>
            </div>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Total Value</span>
                <span className="text-lg font-medium text-gray-900 dark:text-white">
                  ${dashboardSummary.portfolio.value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Gain/Loss</span>
                <span className={dashboardSummary.portfolio.gain >= 0 ? "text-success-600 dark:text-success-400" : "text-danger-600 dark:text-danger-400"}>
                  {dashboardSummary.portfolio.gain >= 0 ? '+' : ''}${Math.abs(dashboardSummary.portfolio.gain).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  {' '}({dashboardSummary.portfolio.gainPercentage >= 0 ? '+' : ''}{dashboardSummary.portfolio.gainPercentage}%)
                </span>
              </div>
              {dashboardSummary.portfolio.trend === 'up' ? (
                <div className="flex items-center text-success-600 dark:text-success-400">
                  <ArrowTrendingUpIcon className="h-5 w-5 mr-1" />
                  <span>{dashboardSummary.portfolio.trendPercentage}% up from last week</span>
                </div>
              ) : (
                <div className="flex items-center text-danger-600 dark:text-danger-400">
                  <ArrowTrendingDownIcon className="h-5 w-5 mr-1" />
                  <span>{dashboardSummary.portfolio.trendPercentage}% down from last week</span>
                </div>
              )}
            </div>
          </div>
        </Link>

        {/* Memory Assistant Module */}
        <Link to="/memory" className="card hover:ring-2 hover:ring-primary-500 transition-all">
          <div className="p-6">
            <div className="flex items-center mb-4">
              <div className="bg-primary-100 dark:bg-primary-900 p-3 rounded-lg">
                <BellAlertIcon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
              </div>
              <h2 className="ml-3 text-xl font-semibold text-gray-900 dark:text-white">Memory Assistant</h2>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Upcoming Events</span>
                <span className="bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 text-sm font-medium py-1 px-2 rounded-full">
                  {dashboardSummary.memory.upcomingEvents}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Birthdays</span>
                <span className="bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 text-sm font-medium py-1 px-2 rounded-full">
                  {dashboardSummary.memory.upcomingBirthdays}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Reminders</span>
                <span className="bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 text-sm font-medium py-1 px-2 rounded-full">
                  {dashboardSummary.memory.reminders}
                </span>
              </div>
            </div>
          </div>
        </Link>

        {/* Email Module */}
        <Link to="/email" className="card hover:ring-2 hover:ring-primary-500 transition-all">
          <div className="p-6">
            <div className="flex items-center mb-4">
              <div className="bg-danger-100 dark:bg-danger-900 p-3 rounded-lg">
                <EnvelopeIcon className="h-6 w-6 text-danger-600 dark:text-danger-400" />
              </div>
              <h2 className="ml-3 text-xl font-semibold text-gray-900 dark:text-white">Email</h2>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Unread</span>
                <span className="bg-danger-100 dark:bg-danger-900 text-danger-800 dark:text-danger-200 text-sm font-medium py-1 px-2 rounded-full">
                  {dashboardSummary.email.unread}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Important</span>
                <span className="bg-warning-100 dark:bg-warning-900 text-warning-800 dark:text-warning-200 text-sm font-medium py-1 px-2 rounded-full">
                  {dashboardSummary.email.important}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Drafts</span>
                <span className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 text-sm font-medium py-1 px-2 rounded-full">
                  {dashboardSummary.email.drafts}
                </span>
              </div>
            </div>
          </div>
        </Link>

        {/* Life Balance Module */}
        <Link to="/life-balance" className="card hover:ring-2 hover:ring-primary-500 transition-all">
          <div className="p-6">
            <div className="flex items-center mb-4">
              <div className="bg-secondary-100 dark:bg-secondary-900 p-3 rounded-lg">
                <ScaleIcon className="h-6 w-6 text-secondary-600 dark:text-secondary-400" />
              </div>
              <h2 className="ml-3 text-xl font-semibold text-gray-900 dark:text-white">Life Balance</h2>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-500 dark:text-gray-400">Overall Score</span>
                <span className="text-lg font-medium text-gray-900 dark:text-white">
                  {dashboardSummary.lifeBalance.score}/{dashboardSummary.lifeBalance.maxScore}
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                <div
                  className="bg-secondary-600 h-2.5 rounded-full"
                  style={{ width: `${(dashboardSummary.lifeBalance.score / dashboardSummary.lifeBalance.maxScore) * 100}%` }}
                ></div>
              </div>
              <div className="grid grid-cols-2 gap-2 mt-2">
                {dashboardSummary.lifeBalance.areas.map(area => (
                  <div key={area.name} className="flex items-center">
                    <div className="w-2 h-2 rounded-full bg-secondary-500 mr-2"></div>
                    <span className="text-sm text-gray-500 dark:text-gray-400">{area.name}: {area.score}/10</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;

import React from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  BanknotesIcon,
  CreditCardIcon,
  ReceiptPercentIcon,
  ChartBarIcon,
  PlusIcon,
} from '@heroicons/react/24/outline';

// Sample data for demonstration - in a real app this would come from API
const financialData = {
  balance: 12450.78,
  income: {
    amount: 5680.25,
    change: 320.15,
    changePercent: 5.97
  },
  expenses: {
    amount: 3245.67,
    change: -125.45,
    changePercent: -3.72
  },
  savings: {
    amount: 2434.58,
    change: 445.60,
    changePercent: 22.40
  },
  recentTransactions: [
    { id: 1, description: 'Grocery Shopping', amount: -87.32, category: 'Food', date: '2025-03-15' },
    { id: 2, description: 'Monthly Salary', amount: 3200.00, category: 'Income', date: '2025-03-01' },
    { id: 3, description: 'Electricity Bill', amount: -142.56, category: 'Utilities', date: '2025-03-10' },
    { id: 4, description: 'Freelance Work', amount: 450.00, category: 'Income', date: '2025-03-08' },
    { id: 5, description: 'Restaurant Dinner', amount: -68.90, category: 'Dining Out', date: '2025-03-14' }
  ],
  topCategories: [
    { name: 'Housing', amount: 1250.00, percentage: 38.5 },
    { name: 'Food', amount: 650.75, percentage: 20.0 },
    { name: 'Transportation', amount: 325.45, percentage: 10.0 },
    { name: 'Utilities', amount: 295.32, percentage: 9.1 },
    { name: 'Entertainment', amount: 225.80, percentage: 7.0 }
  ],
  budgets: [
    { id: 1, category: 'Food', budgeted: 700.00, spent: 650.75, remaining: 49.25 },
    { id: 2, category: 'Entertainment', budgeted: 300.00, spent: 225.80, remaining: 74.20 },
    { id: 3, category: 'Transportation', budgeted: 350.00, spent: 325.45, remaining: 24.55 }
  ]
};

const FinanceOverview: React.FC = () => {
  return (
    <div>
      {/* Page header */}
      <div className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Finance Overview</h1>
          <p className="mt-1 text-gray-600 dark:text-gray-400">
            Track your finances, manage budgets, and analyze spending patterns
          </p>
        </div>
        <div className="mt-4 md:mt-0 flex space-x-3">
          <Link to="/finance/transactions/new" className="btn btn-primary">
            <PlusIcon className="h-5 w-5 mr-2" />
            Add Transaction
          </Link>
        </div>
      </div>

      {/* Financial summary cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Balance card */}
        <div className="card p-6">
          <div className="flex items-center mb-3">
            <div className="bg-primary-100 dark:bg-primary-900 p-2 rounded-lg">
              <BanknotesIcon className="h-5 w-5 text-primary-600 dark:text-primary-400" />
            </div>
            <h3 className="ml-3 text-lg font-medium text-gray-900 dark:text-white">Balance</h3>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            ${financialData.balance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
        </div>

        {/* Income card */}
        <div className="card p-6">
          <div className="flex items-center mb-3">
            <div className="bg-success-100 dark:bg-success-900 p-2 rounded-lg">
              <ReceiptPercentIcon className="h-5 w-5 text-success-600 dark:text-success-400" />
            </div>
            <h3 className="ml-3 text-lg font-medium text-gray-900 dark:text-white">Income</h3>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            ${financialData.income.amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
          <div className="flex items-center mt-2 text-success-600 dark:text-success-400">
            <ArrowTrendingUpIcon className="h-4 w-4 mr-1" />
            <span className="text-sm">
              {financialData.income.changePercent}% from last month
            </span>
          </div>
        </div>

        {/* Expenses card */}
        <div className="card p-6">
          <div className="flex items-center mb-3">
            <div className="bg-danger-100 dark:bg-danger-900 p-2 rounded-lg">
              <CreditCardIcon className="h-5 w-5 text-danger-600 dark:text-danger-400" />
            </div>
            <h3 className="ml-3 text-lg font-medium text-gray-900 dark:text-white">Expenses</h3>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            ${financialData.expenses.amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
          <div className="flex items-center mt-2 text-success-600 dark:text-success-400">
            <ArrowTrendingDownIcon className="h-4 w-4 mr-1" />
            <span className="text-sm">
              {Math.abs(financialData.expenses.changePercent)}% from last month
            </span>
          </div>
        </div>

        {/* Savings card */}
        <div className="card p-6">
          <div className="flex items-center mb-3">
            <div className="bg-primary-100 dark:bg-primary-900 p-2 rounded-lg">
              <ChartBarIcon className="h-5 w-5 text-primary-600 dark:text-primary-400" />
            </div>
            <h3 className="ml-3 text-lg font-medium text-gray-900 dark:text-white">Savings</h3>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            ${financialData.savings.amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
          <div className="flex items-center mt-2 text-success-600 dark:text-success-400">
            <ArrowTrendingUpIcon className="h-4 w-4 mr-1" />
            <span className="text-sm">
              {financialData.savings.changePercent}% from last month
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Transactions */}
        <div className="card">
          <div className="card-header flex justify-between items-center">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Recent Transactions</h3>
            <Link to="/finance/transactions" className="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400">
              View All
            </Link>
          </div>
          <div className="overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Description
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Category
                  </th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Amount
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {financialData.recentTransactions.map((transaction) => (
                  <tr key={transaction.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                      <div>{transaction.description}</div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">{transaction.date}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200">
                        {transaction.category}
                      </span>
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium text-right ${
                      transaction.amount >= 0 
                        ? 'text-success-600 dark:text-success-400' 
                        : 'text-danger-600 dark:text-danger-400'
                    }`}>
                      {transaction.amount >= 0 ? '+' : ''}${Math.abs(transaction.amount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Top Expense Categories */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Top Expense Categories</h3>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              {financialData.topCategories.map((category) => (
                <div key={category.name}>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{category.name}</span>
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      ${category.amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      <span className="text-xs text-gray-500 dark:text-gray-400 ml-1">
                        ({category.percentage}%)
                      </span>
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                    <div 
                      className="bg-primary-600 h-2.5 rounded-full"
                      style={{ width: `${category.percentage}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Budget Status */}
        <div className="card lg:col-span-2">
          <div className="card-header flex justify-between items-center">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Budget Status</h3>
            <Link to="/finance/budgets" className="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400">
              Manage Budgets
            </Link>
          </div>
          <div className="card-body">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {financialData.budgets.map((budget) => {
                const percentage = (budget.spent / budget.budgeted) * 100;
                let statusColor = 'bg-success-600';
                
                if (percentage > 90) {
                  statusColor = 'bg-danger-600';
                } else if (percentage > 75) {
                  statusColor = 'bg-warning-600';
                }
                
                return (
                  <div key={budget.id} className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white">{budget.category}</h4>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        ${budget.spent.toLocaleString('en-US', { minimumFractionDigits: 2 })} of ${budget.budgeted.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mb-2">
                      <div 
                        className={`${statusColor} h-2.5 rounded-full`}
                        style={{ width: `${Math.min(100, percentage)}%` }}
                      ></div>
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {budget.remaining > 0 
                        ? `$${budget.remaining.toLocaleString('en-US', { minimumFractionDigits: 2 })} remaining` 
                        : 'Budget exceeded'}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FinanceOverview;

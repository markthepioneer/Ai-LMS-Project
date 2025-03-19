import React, { useState } from 'react';
import { 
  PlusIcon, 
  FunnelIcon, 
  MagnifyingGlassIcon,
  ArrowDownTrayIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ArrowDownIcon,
  ArrowUpIcon
} from '@heroicons/react/24/outline';
import { Link } from 'react-router-dom';

// Sample data for demonstration - in a real app this would come from API
const transactionsData = [
  { id: 1, description: 'Grocery Shopping', amount: -87.32, category: 'Food', date: '2025-03-15', account: 'Checking' },
  { id: 2, description: 'Monthly Salary', amount: 3200.00, category: 'Income', date: '2025-03-01', account: 'Checking' },
  { id: 3, description: 'Electricity Bill', amount: -142.56, category: 'Utilities', date: '2025-03-10', account: 'Checking' },
  { id: 4, description: 'Freelance Work', amount: 450.00, category: 'Income', date: '2025-03-08', account: 'Savings' },
  { id: 5, description: 'Restaurant Dinner', amount: -68.90, category: 'Dining Out', date: '2025-03-14', account: 'Credit Card' },
  { id: 6, description: 'Gas Station', amount: -45.23, category: 'Transportation', date: '2025-03-12', account: 'Credit Card' },
  { id: 7, description: 'Online Shopping', amount: -125.45, category: 'Shopping', date: '2025-03-09', account: 'Credit Card' },
  { id: 8, description: 'Movie Tickets', amount: -32.50, category: 'Entertainment', date: '2025-03-16', account: 'Credit Card' },
  { id: 9, description: 'Investment Dividend', amount: 78.34, category: 'Income', date: '2025-03-05', account: 'Investment' },
  { id: 10, description: 'Mobile Phone Bill', amount: -65.00, category: 'Utilities', date: '2025-03-08', account: 'Checking' },
  { id: 11, description: 'Coffee Shop', amount: -4.75, category: 'Food', date: '2025-03-17', account: 'Credit Card' },
  { id: 12, description: 'Public Transport', amount: -25.00, category: 'Transportation', date: '2025-03-05', account: 'Checking' },
  { id: 13, description: 'Gym Membership', amount: -50.00, category: 'Health', date: '2025-03-03', account: 'Credit Card' },
  { id: 14, description: 'Bonus Payment', amount: 500.00, category: 'Income', date: '2025-03-10', account: 'Checking' },
  { id: 15, description: 'Internet Bill', amount: -59.99, category: 'Utilities', date: '2025-03-11', account: 'Checking' }
];

// Categories for filtering
const categories = [
  'All Categories', 'Income', 'Food', 'Utilities', 'Transportation', 
  'Entertainment', 'Shopping', 'Dining Out', 'Health'
];

// Accounts for filtering
const accounts = ['All Accounts', 'Checking', 'Savings', 'Credit Card', 'Investment'];

const Transactions: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All Categories');
  const [selectedAccount, setSelectedAccount] = useState('All Accounts');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [sortField, setSortField] = useState('date');
  const [sortDirection, setSortDirection] = useState('desc');
  const itemsPerPage = 10;

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setCurrentPage(1);
  };

  const handleCategoryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedCategory(event.target.value);
    setCurrentPage(1);
  };

  const handleAccountChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedAccount(event.target.value);
    setCurrentPage(1);
  };

  const handleStartDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setStartDate(event.target.value);
    setCurrentPage(1);
  };

  const handleEndDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEndDate(event.target.value);
    setCurrentPage(1);
  };

  const handleSort = (field: string) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  // Filter transactions based on search term, category, account, and date range
  const filteredTransactions = transactionsData.filter(transaction => {
    // Search term filter
    const searchMatch = searchTerm === '' ||
      transaction.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      transaction.category.toLowerCase().includes(searchTerm.toLowerCase());

    // Category filter
    const categoryMatch = selectedCategory === 'All Categories' || transaction.category === selectedCategory;

    // Account filter
    const accountMatch = selectedAccount === 'All Accounts' || transaction.account === selectedAccount;

    // Date range filter
    const dateMatch = (
      (startDate === '' || new Date(transaction.date) >= new Date(startDate)) &&
      (endDate === '' || new Date(transaction.date) <= new Date(endDate))
    );

    return searchMatch && categoryMatch && accountMatch && dateMatch;
  });

  // Sort transactions
  const sortedTransactions = [...filteredTransactions].sort((a, b) => {
    if (sortField === 'date') {
      const dateA = new Date(a.date).getTime();
      const dateB = new Date(b.date).getTime();
      return sortDirection === 'asc' ? dateA - dateB : dateB - dateA;
    } else if (sortField === 'amount') {
      return sortDirection === 'asc' ? a.amount - b.amount : b.amount - a.amount;
    } else if (sortField === 'description') {
      return sortDirection === 'asc' 
        ? a.description.localeCompare(b.description)
        : b.description.localeCompare(a.description);
    } else {
      return 0;
    }
  });

  // Paginate transactions
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = sortedTransactions.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(sortedTransactions.length / itemsPerPage);

  return (
    <div>
      {/* Page header */}
      <div className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Transactions</h1>
          <p className="mt-1 text-gray-600 dark:text-gray-400">
            View and manage your financial transactions
          </p>
        </div>
        <div className="mt-4 md:mt-0 flex space-x-3">
          <Link to="/finance/transactions/new" className="btn btn-primary">
            <PlusIcon className="h-5 w-5 mr-2" />
            Add Transaction
          </Link>
          <button className="btn btn-outline">
            <ArrowDownTrayIcon className="h-5 w-5 mr-2" />
            Export
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-card mb-6 p-4">
        <div className="flex flex-col md:flex-row md:items-center space-y-4 md:space-y-0 md:space-x-4">
          {/* Search */}
          <div className="flex-1">
            <label htmlFor="search" className="sr-only">Search transactions</label>
            <div className="relative rounded-md shadow-sm">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
              </div>
              <input
                type="text"
                id="search"
                className="form-input block w-full pl-10"
                placeholder="Search transactions..."
                value={searchTerm}
                onChange={handleSearch}
              />
            </div>
          </div>

          {/* Category filter */}
          <div className="w-full md:w-48">
            <label htmlFor="category" className="sr-only">Category</label>
            <select
              id="category"
              className="form-select block w-full"
              value={selectedCategory}
              onChange={handleCategoryChange}
            >
              {categories.map((category) => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>

          {/* Account filter */}
          <div className="w-full md:w-48">
            <label htmlFor="account" className="sr-only">Account</label>
            <select
              id="account"
              className="form-select block w-full"
              value={selectedAccount}
              onChange={handleAccountChange}
            >
              {accounts.map((account) => (
                <option key={account} value={account}>{account}</option>
              ))}
            </select>
          </div>

          {/* Date range */}
          <div className="flex space-x-2">
            <div>
              <label htmlFor="start-date" className="sr-only">Start Date</label>
              <input
                type="date"
                id="start-date"
                className="form-input block w-full"
                value={startDate}
                onChange={handleStartDateChange}
              />
            </div>
            <div>
              <label htmlFor="end-date" className="sr-only">End Date</label>
              <input
                type="date"
                id="end-date"
                className="form-input block w-full"
                value={endDate}
                onChange={handleEndDateChange}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="bg-white dark:bg-gray-800 shadow-card rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th 
                  scope="col" 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('date')}
                >
                  <div className="flex items-center">
                    Date
                    <span className="ml-1">
                      {sortField === 'date' && (
                        sortDirection === 'asc' ? (
                          <ArrowUpIcon className="h-4 w-4" />
                        ) : (
                          <ArrowDownIcon className="h-4 w-4" />
                        )
                      )}
                    </span>
                  </div>
                </th>
                <th 
                  scope="col" 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('description')}
                >
                  <div className="flex items-center">
                    Description
                    <span className="ml-1">
                      {sortField === 'description' && (
                        sortDirection === 'asc' ? (
                          <ArrowUpIcon className="h-4 w-4" />
                        ) : (
                          <ArrowDownIcon className="h-4 w-4" />
                        )
                      )}
                    </span>
                  </div>
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Category
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Account
                </th>
                <th 
                  scope="col" 
                  className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider cursor-pointer"
                  onClick={() => handleSort('amount')}
                >
                  <div className="flex items-center justify-end">
                    Amount
                    <span className="ml-1">
                      {sortField === 'amount' && (
                        sortDirection === 'asc' ? (
                          <ArrowUpIcon className="h-4 w-4" />
                        ) : (
                          <ArrowDownIcon className="h-4 w-4" />
                        )
                      )}
                    </span>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {currentItems.map((transaction) => (
                <tr key={transaction.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {transaction.date}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {transaction.description}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200">
                      {transaction.category}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {transaction.account}
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
        
        {/* Pagination */}
        <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <div className="text-sm text-gray-700 dark:text-gray-300">
            Showing <span className="font-medium">{indexOfFirstItem + 1}</span> to <span className="font-medium">
              {Math.min(indexOfLastItem, sortedTransactions.length)}
            </span> of <span className="font-medium">{sortedTransactions.length}</span> transactions
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              className={`btn btn-outline p-2 ${currentPage === 1 ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <ChevronLeftIcon className="h-5 w-5" />
            </button>
            <button
              onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
              disabled={currentPage === totalPages}
              className={`btn btn-outline p-2 ${currentPage === totalPages ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <ChevronRightIcon className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Transactions;

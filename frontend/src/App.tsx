import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import DashboardLayout from './layouts/DashboardLayout';
import AuthLayout from './layouts/AuthLayout';

// Auth Pages
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import ResetPassword from './pages/auth/ResetPassword';

// Dashboard Pages
import Dashboard from './pages/dashboard/Dashboard';

// Finance Pages
import FinanceOverview from './pages/finance/FinanceOverview';
import Transactions from './pages/finance/Transactions';
import Budgets from './pages/finance/Budgets';
import FinancialInsights from './pages/finance/FinancialInsights';

// Health Pages
import HealthOverview from './pages/health/HealthOverview';
import SleepTracking from './pages/health/SleepTracking';
import ExerciseTracking from './pages/health/ExerciseTracking';
import HealthInsights from './pages/health/HealthInsights';

// Task Pages
import TaskOverview from './pages/tasks/TaskOverview';
import TaskCalendar from './pages/tasks/TaskCalendar';
import TaskAnalytics from './pages/tasks/TaskAnalytics';

// Portfolio Pages
import PortfolioOverview from './pages/portfolio/PortfolioOverview';
import Investments from './pages/portfolio/Investments';
import PortfolioAnalytics from './pages/portfolio/PortfolioAnalytics';

// Memory Pages
import MemoryOverview from './pages/memory/MemoryOverview';
import Contacts from './pages/memory/Contacts';
import Reminders from './pages/memory/Reminders';
import Events from './pages/memory/Events';

// Email Pages
import EmailOverview from './pages/email/EmailOverview';
import EmailInbox from './pages/email/EmailInbox';
import EmailTemplates from './pages/email/EmailTemplates';
import EmailAnalytics from './pages/email/EmailAnalytics';

// Life Balance Pages
import LifeBalanceOverview from './pages/lifebalance/LifeBalanceOverview';
import LifeGoals from './pages/lifebalance/LifeGoals';
import LifeAnalytics from './pages/lifebalance/LifeAnalytics';

// Profile Pages
import UserProfile from './pages/profile/UserProfile';
import UserSettings from './pages/profile/UserSettings';

// Error Pages
import NotFound from './pages/errors/NotFound';
import ServerError from './pages/errors/ServerError';

const App = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-700 dark:text-gray-300 text-lg">Loading your life dashboard<span className="loading-dots"></span></p>
        </div>
      </div>
    );
  }

  return (
    <Routes>
      {/* Auth Routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" replace />} />
        <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" replace />} />
        <Route path="/forgot-password" element={!isAuthenticated ? <ForgotPassword /> : <Navigate to="/dashboard" replace />} />
        <Route path="/reset-password" element={!isAuthenticated ? <ResetPassword /> : <Navigate to="/dashboard" replace />} />
      </Route>

      {/* Dashboard Routes */}
      <Route element={<DashboardLayout />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" replace />} />
        
        {/* Finance Module Routes */}
        <Route path="/finance" element={isAuthenticated ? <FinanceOverview /> : <Navigate to="/login" replace />} />
        <Route path="/finance/transactions" element={isAuthenticated ? <Transactions /> : <Navigate to="/login" replace />} />
        <Route path="/finance/budgets" element={isAuthenticated ? <Budgets /> : <Navigate to="/login" replace />} />
        <Route path="/finance/insights" element={isAuthenticated ? <FinancialInsights /> : <Navigate to="/login" replace />} />
        
        {/* Health Module Routes */}
        <Route path="/health" element={isAuthenticated ? <HealthOverview /> : <Navigate to="/login" replace />} />
        <Route path="/health/sleep" element={isAuthenticated ? <SleepTracking /> : <Navigate to="/login" replace />} />
        <Route path="/health/exercise" element={isAuthenticated ? <ExerciseTracking /> : <Navigate to="/login" replace />} />
        <Route path="/health/insights" element={isAuthenticated ? <HealthInsights /> : <Navigate to="/login" replace />} />
        
        {/* Task Module Routes */}
        <Route path="/tasks" element={isAuthenticated ? <TaskOverview /> : <Navigate to="/login" replace />} />
        <Route path="/tasks/calendar" element={isAuthenticated ? <TaskCalendar /> : <Navigate to="/login" replace />} />
        <Route path="/tasks/analytics" element={isAuthenticated ? <TaskAnalytics /> : <Navigate to="/login" replace />} />
        
        {/* Portfolio Module Routes */}
        <Route path="/portfolio" element={isAuthenticated ? <PortfolioOverview /> : <Navigate to="/login" replace />} />
        <Route path="/portfolio/investments" element={isAuthenticated ? <Investments /> : <Navigate to="/login" replace />} />
        <Route path="/portfolio/analytics" element={isAuthenticated ? <PortfolioAnalytics /> : <Navigate to="/login" replace />} />
        
        {/* Memory Module Routes */}
        <Route path="/memory" element={isAuthenticated ? <MemoryOverview /> : <Navigate to="/login" replace />} />
        <Route path="/memory/contacts" element={isAuthenticated ? <Contacts /> : <Navigate to="/login" replace />} />
        <Route path="/memory/reminders" element={isAuthenticated ? <Reminders /> : <Navigate to="/login" replace />} />
        <Route path="/memory/events" element={isAuthenticated ? <Events /> : <Navigate to="/login" replace />} />
        
        {/* Email Module Routes */}
        <Route path="/email" element={isAuthenticated ? <EmailOverview /> : <Navigate to="/login" replace />} />
        <Route path="/email/inbox" element={isAuthenticated ? <EmailInbox /> : <Navigate to="/login" replace />} />
        <Route path="/email/templates" element={isAuthenticated ? <EmailTemplates /> : <Navigate to="/login" replace />} />
        <Route path="/email/analytics" element={isAuthenticated ? <EmailAnalytics /> : <Navigate to="/login" replace />} />
        
        {/* Life Balance Module Routes */}
        <Route path="/life-balance" element={isAuthenticated ? <LifeBalanceOverview /> : <Navigate to="/login" replace />} />
        <Route path="/life-balance/goals" element={isAuthenticated ? <LifeGoals /> : <Navigate to="/login" replace />} />
        <Route path="/life-balance/analytics" element={isAuthenticated ? <LifeAnalytics /> : <Navigate to="/login" replace />} />
        
        {/* Profile Routes */}
        <Route path="/profile" element={isAuthenticated ? <UserProfile /> : <Navigate to="/login" replace />} />
        <Route path="/settings" element={isAuthenticated ? <UserSettings /> : <Navigate to="/login" replace />} />
      </Route>

      {/* Error Routes */}
      <Route path="/server-error" element={<ServerError />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default App;

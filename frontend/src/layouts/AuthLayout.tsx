import { Outlet } from 'react-router-dom';
import { useTheme } from '../hooks/useTheme';

const AuthLayout = () => {
  const { theme } = useTheme();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-primary-600 dark:text-primary-500">
              AI Life Management System
            </h2>
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              The intelligent way to manage every aspect of your life
            </p>
          </div>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white dark:bg-gray-800 py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <Outlet />
          </div>
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              © {new Date().getFullYear()} AI Life Management System. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;

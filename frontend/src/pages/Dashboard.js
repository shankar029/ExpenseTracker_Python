import { useEffect, useState } from 'react';
import ExpenseForm from '../components/Expenses/ExpenseForm';
import ExpenseList from '../components/Expenses/ExpenseList';
import Header from '../components/Layout/Header';
import '../components/Layout/Layout.css';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [mounted, setMounted] = useState(false);
  const { isAuthenticated, user } = useAuth();

  useEffect(() => {
    // Small delay to ensure auth state is fully settled
    const timer = setTimeout(() => {
      setMounted(true);
    }, 100);
    return () => clearTimeout(timer);
  }, []);

  // Don't render until we're sure auth state is settled
  if (!mounted || !isAuthenticated || !user) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <span className="loading-text">Loading dashboard...</span>
      </div>
    );
  }

  const handleExpenseAdded = () => {
    // Trigger refresh of expense list
    setRefreshTrigger(prev => prev + 1);
  };

  const handleExpenseEdit = (expense) => {
    // For now, just log the expense to edit
    // In a full implementation, you might open an edit modal
    console.log('Edit expense:', expense);
  };

  return (
    <div className="main-layout">
      <Header />
      <main className="main-content">
        <div className="container">
          <div className="page-header">
            <h1 className="page-title">Dashboard</h1>
            <p className="page-subtitle">
              Track and manage your expenses
            </p>
          </div>

          <div className="dashboard-content">
            <ExpenseForm onExpenseAdded={handleExpenseAdded} />
            <ExpenseList
              refreshTrigger={refreshTrigger}
              onEdit={handleExpenseEdit}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
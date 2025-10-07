import { useEffect, useState } from 'react';
import api from '../../services/api';
import { getErrorMessage } from '../../utils/helpers';
import Button from '../Common/Button';
import ExpenseItem from './ExpenseItem';
import './Expenses.css';

const ExpenseList = ({ refreshTrigger, onEdit }) => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Small delay to ensure token is stored after login
    const timer = setTimeout(() => {
      fetchExpenses();
    }, 100);

    return () => clearTimeout(timer);
  }, [refreshTrigger]);

  const fetchExpenses = async () => {
    try {
      setLoading(true);
      setError('');

      // Debug: Check if token exists
      const token = localStorage.getItem('token');
      console.log('Token before expenses request:', token ? 'exists' : 'missing');

      const response = await api.get('/expenses');
      setExpenses(response.data.expenses || []);
    } catch (err) {
      console.error('Fetch expenses error:', err);
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (expenseId) => {
    if (!window.confirm('Are you sure you want to delete this expense?')) {
      return;
    }

    try {
      await api.delete(`/expenses/${expenseId}`);
      setExpenses(expenses.filter(expense => expense.id !== expenseId));
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  if (loading) {
    return (
      <div className="expense-list__loading">
        <div className="spinner"></div>
        <span className="loading-text">Loading expenses...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="expense-list__error">
        <div className="error-message">
          {error}
          <Button
            variant="outline"
            size="small"
            onClick={fetchExpenses}
            className="retry-btn"
          >
            Retry
          </Button>
        </div>
      </div>
    );
  }

  if (expenses.length === 0) {
    return (
      <div className="expense-list__empty">
        <div className="empty-state">
          <div className="empty-state__icon">📝</div>
          <h3 className="empty-state__title">No expenses yet</h3>
          <p className="empty-state__description">
            Start tracking your expenses by adding your first one above.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="expense-list">
      <div className="expense-list__header">
        <h3 className="expense-list__title">
          Your Expenses ({expenses.length})
        </h3>
      </div>

      <div className="expense-grid">
        {expenses.map(expense => (
          <ExpenseItem
            key={expense.id}
            expense={expense}
            onDelete={handleDelete}
            onEdit={onEdit}
          />
        ))}
      </div>
    </div>
  );
};

export default ExpenseList;
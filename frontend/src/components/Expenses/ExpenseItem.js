import React from 'react';
import Button from '../Common/Button';
import { formatCurrency, formatDate } from '../../utils/helpers';
import './Expenses.css';

const ExpenseItem = ({ expense, onDelete, onEdit }) => {
  const handleDelete = () => {
    onDelete(expense.id);
  };

  const handleEdit = () => {
    if (onEdit) {
      onEdit(expense);
    }
  };

  const getCategoryIcon = (category) => {
    const icons = {
      'Food': '🍽️',
      'Transportation': '🚗',
      'Entertainment': '🎬',
      'Healthcare': '🏥',
      'Shopping': '🛍️',
      'Utilities': '🏠',
      'Other': '📦'
    };
    return icons[category] || '📦';
  };

  const getCategoryColor = (category) => {
    const colors = {
      'Food': '#ef4444',
      'Transportation': '#3b82f6',
      'Entertainment': '#8b5cf6',
      'Healthcare': '#10b981',
      'Shopping': '#f59e0b',
      'Utilities': '#6b7280',
      'Other': '#64748b'
    };
    return colors[category] || '#64748b';
  };

  return (
    <div className="expense-item">
      <div className="expense-item__header">
        <div 
          className="expense-item__category"
          style={{ backgroundColor: getCategoryColor(expense.category) }}
        >
          <span className="expense-item__category-icon">
            {getCategoryIcon(expense.category)}
          </span>
          <span className="expense-item__category-name">
            {expense.category}
          </span>
        </div>
        <div className="expense-item__amount">
          {formatCurrency(expense.amount)}
        </div>
      </div>

      <div className="expense-item__content">
        <h4 className="expense-item__description">
          {expense.description}
        </h4>
        <p className="expense-item__date">
          {formatDate(expense.date)}
        </p>
      </div>

      <div className="expense-item__actions">
        {onEdit && (
          <Button
            variant="outline"
            size="small"
            onClick={handleEdit}
            className="expense-item__edit-btn"
          >
            Edit
          </Button>
        )}
        <Button
          variant="danger"
          size="small"
          onClick={handleDelete}
          className="expense-item__delete-btn"
        >
          Delete
        </Button>
      </div>
    </div>
  );
};

export default ExpenseItem;
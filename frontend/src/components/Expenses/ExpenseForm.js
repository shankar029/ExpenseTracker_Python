import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import api from '../../services/api';
import Button from '../Common/Button';
import Input from '../Common/Input';
import { EXPENSE_CATEGORIES } from '../../utils/constants';
import { getErrorMessage, getTodayDate, isValidAmount } from '../../utils/helpers';
import './Expenses.css';

const ExpenseForm = ({ onExpenseAdded }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm({
    defaultValues: {
      date: getTodayDate()
    }
  });

  const onSubmit = async (data) => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const expenseData = {
        amount: parseFloat(data.amount),
        description: data.description.trim(),
        category: data.category,
        date: data.date
      };

      const response = await api.post('/expenses', expenseData);
      setSuccess('Expense added successfully!');
      reset({ date: getTodayDate() });
      
      if (onExpenseAdded) {
        onExpenseAdded(response.data);
      }

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="expense-form">
      <div className="expense-form__header">
        <h3 className="expense-form__title">Add New Expense</h3>
        <p className="expense-form__subtitle">Track your spending</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="expense-form__form">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {success && (
          <div className="success-message">
            {success}
          </div>
        )}

        <div className="expense-form__row">
          <Input
            label="Amount"
            type="number"
            name="amount"
            placeholder="0.00"
            required
            step="0.01"
            min="0"
            error={errors.amount?.message}
            {...register('amount', {
              required: 'Amount is required',
              validate: (value) => 
                isValidAmount(value) || 'Please enter a valid amount greater than 0'
            })}
          />

          <div className="input-group">
            <label htmlFor="category" className="input__label">
              Category <span className="input__required">*</span>
            </label>
            <select
              id="category"
              name="category"
              className={`select ${errors.category ? 'input--error' : ''}`}
              {...register('category', {
                required: 'Category is required'
              })}
            >
              <option value="">Select category</option>
              {EXPENSE_CATEGORIES.map(category => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
            {errors.category && (
              <span className="input__error">{errors.category.message}</span>
            )}
          </div>
        </div>

        <Input
          label="Description"
          type="text"
          name="description"
          placeholder="What did you spend on?"
          required
          error={errors.description?.message}
          {...register('description', {
            required: 'Description is required',
            minLength: {
              value: 3,
              message: 'Description must be at least 3 characters'
            },
            maxLength: {
              value: 255,
              message: 'Description must be less than 255 characters'
            }
          })}
        />

        <Input
          label="Date"
          type="date"
          name="date"
          required
          error={errors.date?.message}
          {...register('date', {
            required: 'Date is required'
          })}
        />

        <Button
          type="submit"
          variant="primary"
          size="large"
          loading={loading}
          className="expense-form__submit"
        >
          Add Expense
        </Button>
      </form>
    </div>
  );
};

export default ExpenseForm;
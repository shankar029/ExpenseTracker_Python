import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Button from '../Common/Button';
import Input from '../Common/Input';
import { getErrorMessage, isValidEmail } from '../../utils/helpers';
import './AuthForm.css';

const Signup = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { signup } = useAuth();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors }
  } = useForm();

  const password = watch('password');

  const onSubmit = async (data) => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await signup({
        username: data.username,
        email: data.email,
        password: data.password
      });
      setSuccess('Account created successfully! Please sign in.');
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2 className="auth-title">Sign Up</h2>
          <p className="auth-subtitle">Create your Expense Tracker account</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="auth-form">
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

          <Input
            label="Username"
            type="text"
            name="username"
            placeholder="Choose a username"
            required
            error={errors.username?.message}
            {...register('username', {
              required: 'Username is required',
              minLength: {
                value: 3,
                message: 'Username must be at least 3 characters'
              }
            })}
          />

          <Input
            label="Email"
            type="email"
            name="email"
            placeholder="Enter your email address"
            required
            error={errors.email?.message}
            {...register('email', {
              required: 'Email is required',
              validate: (value) => 
                isValidEmail(value) || 'Please enter a valid email address'
            })}
          />

          <Input
            label="Password"
            type="password"
            name="password"
            placeholder="Create a password"
            required
            error={errors.password?.message}
            {...register('password', {
              required: 'Password is required',
              minLength: {
                value: 6,
                message: 'Password must be at least 6 characters'
              }
            })}
          />

          <Input
            label="Confirm Password"
            type="password"
            name="confirmPassword"
            placeholder="Confirm your password"
            required
            error={errors.confirmPassword?.message}
            {...register('confirmPassword', {
              required: 'Please confirm your password',
              validate: (value) => 
                value === password || 'Passwords do not match'
            })}
          />

          <Button
            type="submit"
            variant="primary"
            size="large"
            loading={loading}
            className="auth-submit-btn"
          >
            Sign Up
          </Button>
        </form>

        <div className="auth-footer">
          <p>
            Already have an account?{' '}
            <Link to="/login" className="auth-link">
              Sign in here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;
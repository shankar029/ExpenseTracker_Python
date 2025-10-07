import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { getErrorMessage } from '../../utils/helpers';
import Button from '../Common/Button';
import Input from '../Common/Input';
import './AuthForm.css';

const Login = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm();

  const onSubmit = async (data) => {
    setLoading(true);
    setError('');

    try {
      await login(data);
      // Small delay to ensure auth state is fully updated
      setTimeout(() => {
        navigate('/dashboard');
      }, 150);
    } catch (err) {
      setError(getErrorMessage(err));
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2 className="auth-title">Sign In</h2>
          <p className="auth-subtitle">Welcome back to Expense Tracker</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="auth-form">
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <Input
            label="Username"
            type="text"
            name="username"
            placeholder="Enter your username"
            required
            error={errors.username?.message}
            {...register('username', {
              required: 'Username is required'
            })}
          />

          <Input
            label="Password"
            type="password"
            name="password"
            placeholder="Enter your password"
            required
            error={errors.password?.message}
            {...register('password', {
              required: 'Password is required'
            })}
          />

          <Button
            type="submit"
            variant="primary"
            size="large"
            loading={loading}
            className="auth-submit-btn"
          >
            Sign In
          </Button>
        </form>

        <div className="auth-footer">
          <p>
            Don't have an account?{' '}
            <Link to="/signup" className="auth-link">
              Sign up here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
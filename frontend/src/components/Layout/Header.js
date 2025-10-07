import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import Button from '../Common/Button';
import Navigation from './Navigation';
import './Layout.css';

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <header className="header">
      <div className="header__container">
        <div className="header__brand">
          <h1 className="header__logo">
            💰 Expense Tracker
          </h1>
        </div>

        <Navigation />

        <div className="header__user">
          {user && (
            <div className="header__user-info">
              <span className="header__username">
                Welcome, {user.username}
              </span>
              <Button
                variant="outline"
                size="small"
                onClick={handleLogout}
                className="header__logout-btn"
              >
                Logout
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
# Expense Tracker Frontend

A React-based frontend application for tracking personal expenses with a modern, responsive design using flexbox grid layout.

## Features

- **User Authentication**: Secure login/signup with JWT tokens
- **Expense Management**: Add, view, and delete expenses
- **Responsive Design**: Flexbox-based grid layout that works on all devices
- **Modern UI**: Clean interface with category-coded expenses
- **Real-time Updates**: Dynamic expense list updates
- **Form Validation**: Client-side validation with user-friendly error messages

## Technology Stack

- **React 18** with functional components and hooks
- **React Router** for navigation and protected routes
- **React Hook Form** for form management and validation
- **Axios** for API communication
- **CSS Flexbox** for responsive grid layouts
- **JWT** token-based authentication

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend server running on http://localhost:5000

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Backend Integration

The frontend is configured to connect to the Flask backend API at `http://localhost:5000`. Make sure the backend server is running before starting the frontend application.

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm run build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm run eject` - Ejects from Create React App (one-way operation)

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── Login.js
│   │   │   ├── Signup.js
│   │   │   └── AuthForm.css
│   │   ├── Expenses/
│   │   │   ├── ExpenseList.js
│   │   │   ├── ExpenseForm.js
│   │   │   ├── ExpenseItem.js
│   │   │   └── Expenses.css
│   │   ├── Layout/
│   │   │   ├── Header.js
│   │   │   ├── Navigation.js
│   │   │   └── Layout.css
│   │   └── Common/
│   │       ├── Button.js
│   │       ├── Input.js
│   │       └── Common.css
│   ├── pages/
│   │   ├── Dashboard.js
│   │   ├── Login.js
│   │   └── Signup.js
│   ├── services/
│   │   ├── api.js
│   │   └── auth.js
│   ├── utils/
│   │   ├── constants.js
│   │   └── helpers.js
│   ├── context/
│   │   └── AuthContext.js
│   ├── App.js
│   ├── App.css
│   └── index.js
├── package.json
└── README.md
```

## Key Features

### Authentication
- Secure user registration and login
- JWT token management with automatic refresh
- Protected routes that require authentication
- Persistent login state across browser sessions

### Expense Management
- Add new expenses with amount, description, category, and date
- View expenses in a responsive grid layout
- Delete expenses with confirmation
- Category-coded expenses with icons and colors
- Form validation for all inputs

### Responsive Design
- Mobile-first responsive design
- Flexbox-based grid layout that adapts to screen size:
  - Mobile: 1 column
  - Tablet: 2 columns  
  - Desktop: 3+ columns
- Touch-friendly interface on mobile devices

### UI/UX
- Modern, clean interface design
- Loading states and error handling
- Success/error notifications
- Intuitive navigation and user feedback

## API Integration

The frontend integrates with the following backend endpoints:

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Expenses
- `GET /api/expenses` - Get user's expenses
- `POST /api/expenses` - Create new expense
- `DELETE /api/expenses/{id}` - Delete expense

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development

### Adding New Components

1. Create component files in the appropriate directory under `src/components/`
2. Add corresponding CSS files for styling
3. Export components from their respective directories
4. Import and use in parent components

### Adding New Pages

1. Create page components in `src/pages/`
2. Add routes in `App.js`
3. Update navigation in `Navigation.js` if needed

### Styling Guidelines

- Use CSS flexbox for layouts
- Follow mobile-first responsive design
- Use CSS custom properties for consistent theming
- Keep styles modular and component-specific

## Contributing

1. Follow the existing code structure and patterns
2. Add proper error handling for new features
3. Ensure responsive design for all new components
4. Test thoroughly on different screen sizes

## License

This project is part of the Expense Tracker demo application.
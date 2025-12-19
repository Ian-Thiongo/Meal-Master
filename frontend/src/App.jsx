import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
  const { user } = useAuth();

  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<Home />} />
      
      {/* Auth routes - redirect to dashboard if already logged in */}
      <Route 
        path="/login" 
        element={user ? <Navigate to="/dashboard" /> : <Login />} 
      />
      <Route 
        path="/signup" 
        element={user ? <Navigate to="/dashboard" /> : <Signup />} 
      />
      
      {/* Protected routes - require login */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      
      {/* Catch all - redirect to home */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

export default App;
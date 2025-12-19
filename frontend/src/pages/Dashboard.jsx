import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <nav className="dashboard-nav">
        <h1>Meal Master</h1>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </nav>

      <div className="dashboard-content">
        <div className="welcome-section">
          <h2>Welcome back, {user?.username}! 👋</h2>
          <p>Your personalized meal planning dashboard</p>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">🎯</div>
            <div className="stat-info">
              <h3>Daily Target</h3>
              <p className="stat-value">
                {user?.tdee ? `${Math.round(user.tdee)} kcal` : 'Not set'}
              </p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⚖️</div>
            <div className="stat-info">
              <h3>Weight</h3>
              <p className="stat-value">
                {user?.weight_kg ? `${user.weight_kg} kg` : 'Not set'}
              </p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📏</div>
            <div className="stat-info">
              <h3>Height</h3>
              <p className="stat-value">
                {user?.height_cm ? `${user.height_cm} cm` : 'Not set'}
              </p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🏃</div>
            <div className="stat-info">
              <h3>Activity Level</h3>
              <p className="stat-value">
                {user?.activity_level ? 
                  user.activity_level.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) 
                  : 'Not set'}
              </p>
            </div>
          </div>
        </div>

        <div className="action-cards">
          <div className="action-card">
            <h3>🔍 Search Foods</h3>
            <p>Find foods from our database of 300,000+ items</p>
            <button className="action-btn">Coming Soon</button>
          </div>

          <div className="action-card">
            <h3>📊 Today's Meals</h3>
            <p>View and manage your meal plan for today</p>
            <button className="action-btn">Coming Soon</button>
          </div>

          <div className="action-card">
            <h3>📅 History</h3>
            <p>View your past meal plans and progress</p>
            <button className="action-btn">Coming Soon</button>
          </div>

          <div className="action-card">
            <h3>⚙️ Profile Settings</h3>
            <p>Update your personal information and goals</p>
            <button className="action-btn">Coming Soon</button>
          </div>
        </div>

        {!user?.tdee && (
          <div className="alert-box">
            <strong>⚠️ Complete Your Profile</strong>
            <p>Add your weight, height, age, gender, and activity level to calculate your daily calorie target!</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
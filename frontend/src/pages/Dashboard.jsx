import { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import "./Dashboard.css";

function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  
  const [dailyStatus, setDailyStatus] = useState(null);
  const [mealSuggestions, setMealSuggestions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('breakfast');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    const token = localStorage.getItem('token');
    if (!token || !user?.tdee) {
      setLoading(false);
      return;
    }

    try {
      // Get current hour for time-aware greeting
      const currentHour = new Date().getHours();
      
      // Fetch daily status
      const statusResponse = await fetch(
        `http://localhost:5000/api/food/daily-status?hour=${currentHour}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      if (statusResponse.ok) {
        const statusData = await statusResponse.json();
        setDailyStatus(statusData);
      }

      // Fetch meal suggestions
      const suggestionsResponse = await fetch(
        'http://localhost:5000/api/food/meal-plan-suggestions',
        { headers: { Authorization: `Bearer ${token}` } }
      );
      if (suggestionsResponse.ok) {
        const suggestionsData = await suggestionsResponse.json();
        setMealSuggestions(suggestionsData);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="dashboard">
      {/* Navigation */}
      <nav className="dashboard-nav">
        <div className="nav-container">
          <Link to="/" className="nav-logo">
            <span className="logo-icon">🍽️</span>
            <span className="logo-text">Meal Master</span>
          </Link>
          
          <div className="nav-actions">
            <Link to="/profile" className="nav-link">
              <span className="nav-avatar">{user?.username?.charAt(0).toUpperCase()}</span>
              <span className="nav-username">{user?.username}</span>
            </Link>
            <button onClick={handleLogout} className="btn btn-ghost">
              Sign Out
            </button>
          </div>
        </div>
      </nav>

      <main className="dashboard-main">
        <div className="dashboard-container">
          {/* Time-Aware Welcome Section */}
          <div className="welcome-section">
            <div className="welcome-content">
              <span className="welcome-tag">Dashboard</span>
              <h1 className="welcome-title">
                {dailyStatus?.greeting || `Welcome back, ${user?.username}!`}
              </h1>
              <p className="welcome-subtitle">
                {dailyStatus?.prompt || "Your personalized nutrition command center"}
              </p>
            </div>
          </div>

          {/* Daily Progress Card */}
          {user?.tdee && dailyStatus && (
            <div className="progress-section">
              <h2 className="section-label">Today's Progress</h2>
              <div className="progress-card">
                <div className="progress-header">
                  <div className="progress-calories">
                    <span className="consumed">{dailyStatus.consumed_calories}</span>
                    <span className="divider">/</span>
                    <span className="target">{dailyStatus.daily_target} kcal</span>
                  </div>
                  <span className="remaining-badge">
                    {dailyStatus.remaining_calories} kcal remaining
                  </span>
                </div>
                <div className="progress-bar-container">
                  <div 
                    className="progress-bar-fill"
                    style={{ width: `${Math.min(dailyStatus.progress_percent, 100)}%` }}
                  />
                </div>
                <p className="progress-hint">
                  {dailyStatus.progress_percent >= 100 
                    ? "🎉 You've reached your daily target!" 
                    : dailyStatus.prompt}
                </p>
              </div>
            </div>
          )}

          {/* Stats Grid */}
          <div className="stats-section">
            <h2 className="section-label">Your Stats</h2>
            <div className="stats-grid">
              <div className="stat-card stat-card-highlight">
                <div className="stat-icon-wrapper">
                  <span className="stat-icon">🎯</span>
                </div>
                <div className="stat-content">
                  <span className="stat-label">Daily Target</span>
                  <span className="stat-value">
                    {user?.tdee ? `${Math.round(user.tdee)} kcal` : "Not set"}
                  </span>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon-wrapper">
                  <span className="stat-icon">⚖️</span>
                </div>
                <div className="stat-content">
                  <span className="stat-label">Weight</span>
                  <span className="stat-value">
                    {user?.weight_kg ? `${user.weight_kg} kg` : "—"}
                  </span>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon-wrapper">
                  <span className="stat-icon">📏</span>
                </div>
                <div className="stat-content">
                  <span className="stat-label">Height</span>
                  <span className="stat-value">
                    {user?.height_cm ? `${user.height_cm} cm` : "—"}
                  </span>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon-wrapper">
                  <span className="stat-icon">{user?.is_vegan ? "🌱" : user?.is_vegetarian ? "🥬" : "🏃"}</span>
                </div>
                <div className="stat-content">
                  <span className="stat-label">Diet</span>
                  <span className="stat-value stat-value-sm">
                    {user?.is_vegan ? "Vegan" : user?.is_vegetarian ? "Vegetarian" : "Regular"}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Meal Suggestions Section */}
          {user?.tdee && mealSuggestions && (
            <div className="suggestions-section">
              <h2 className="section-label">
                Today's Meal Suggestions
                {mealSuggestions.is_vegan && <span className="veg-badge">🌱 Vegan</span>}
                {!mealSuggestions.is_vegan && mealSuggestions.is_vegetarian && <span className="veg-badge">🥬 Vegetarian</span>}
              </h2>
              
              <div className="meal-tabs">
                <button 
                  className={`meal-tab ${activeTab === 'breakfast' ? 'active' : ''}`}
                  onClick={() => setActiveTab('breakfast')}
                >
                  ☀️ Breakfast
                  <span className="tab-calories">{mealSuggestions.meal_targets.breakfast} kcal</span>
                </button>
                <button 
                  className={`meal-tab ${activeTab === 'lunch' ? 'active' : ''}`}
                  onClick={() => setActiveTab('lunch')}
                >
                  🌤️ Lunch
                  <span className="tab-calories">{mealSuggestions.meal_targets.lunch} kcal</span>
                </button>
                <button 
                  className={`meal-tab ${activeTab === 'dinner' ? 'active' : ''}`}
                  onClick={() => setActiveTab('dinner')}
                >
                  🌙 Dinner
                  <span className="tab-calories">{mealSuggestions.meal_targets.dinner} kcal</span>
                </button>
              </div>

              <div className="suggestions-grid">
                {mealSuggestions.suggestions[activeTab]?.map((food, index) => (
                  <div key={index} className="suggestion-card">
                    <div className="suggestion-header">
                      <h4>{food.name}</h4>
                      <span className="suggestion-calories">{food.suggested_calories} kcal</span>
                    </div>
                    <div className="suggestion-macros">
                      <span className="macro protein">P: {food.protein}g</span>
                      <span className="macro carbs">C: {food.carbs}g</span>
                      <span className="macro fat">F: {food.fat}g</span>
                    </div>
                    <p className="suggestion-serving">
                      Suggested: {food.suggested_servings} serving(s)
                    </p>
                    <button 
                      className="btn btn-primary btn-sm"
                      onClick={() => navigate('/search')}
                    >
                      Add to Meal Plan
                    </button>
                  </div>
                ))}
                {(!mealSuggestions.suggestions[activeTab] || mealSuggestions.suggestions[activeTab].length === 0) && (
                  <p className="no-suggestions">No suggestions available. Try refreshing!</p>
                )}
              </div>
            </div>
          )}

          {/* Action Cards */}
          <div className="actions-section">
            <h2 className="section-label">Quick Actions</h2>
            <div className="actions-grid">
              <div className="action-card" onClick={() => navigate("/search")}>
                <div className="action-icon">🔍</div>
                <div className="action-content">
                  <h3>Search Foods</h3>
                  <p>Find foods from our database of 300,000+ items</p>
                </div>
                <span className="action-arrow">→</span>
              </div>

              <div className="action-card" onClick={() => navigate("/search")}>
                <div className="action-icon">📊</div>
                <div className="action-content">
                  <h3>Today's Meals</h3>
                  <p>View and manage your meal plan for today</p>
                </div>
                <span className="action-arrow">→</span>
              </div>

              <div className="action-card" onClick={() => navigate("/profile")}>
                <div className="action-icon">⚙️</div>
                <div className="action-content">
                  <h3>Profile Settings</h3>
                  <p>Update your personal information and goals</p>
                </div>
                <span className="action-arrow">→</span>
              </div>
            </div>
          </div>

          {/* Alert Box */}
          {!user?.tdee && (
            <div className="alert-box">
              <div className="alert-icon">⚠️</div>
              <div className="alert-content">
                <strong>Complete Your Profile</strong>
                <p>
                  Add your weight, height, age, gender, and activity level to
                  calculate your daily calorie target and get meal recommendations!
                </p>
              </div>
              <button className="btn btn-primary" onClick={() => navigate("/profile")}>
                Update Profile
                <span className="btn-arrow">→</span>
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default Dashboard;

import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Home.css';

function Home() {
  const { user } = useAuth();

  const scrollToFeatures = () => {
    document.getElementById('features').scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="home">
      <nav className="home-nav">
        <h1>Meal Master</h1>
        <div className="nav-links">
          {user ? (
            <Link to="/dashboard" className="nav-btn primary">
              Go to Dashboard
            </Link>
          ) : (
            <>
              <Link to="/login" className="nav-btn">
                Login
              </Link>
              <Link to="/signup" className="nav-btn primary">
                Sign Up
              </Link>
            </>
          )}
        </div>
      </nav>

      {/* First Page - Hero */}
      <div className="hero-section">
        <div className="hero">
          <h1>Plan Your Perfect Meals</h1>
          <p>Calculate your daily calorie needs, search from 300,000+ foods, and track your nutrition goals</p>
          {!user && (
            <Link to="/signup" className="cta-btn">
              Get Started Free
            </Link>
          )}
        </div>

        <div className="scroll-indicator" onClick={scrollToFeatures}>
          <span>Discover Features</span>
          <div className="arrow">↓</div>
        </div>
      </div>

      {/* Second Page - Features */}
      <div className="features-section" id="features">
        <h2>Why Choose Meal Master?</h2>
        <div className="features">
          <div className="feature">
            <div className="feature-icon">🎯</div>
            <h3>Calculate TDEE</h3>
            <p>Accurately calculate your Total Daily Energy Expenditure based on the Mifflin-St Jeor equation</p>
          </div>

          <div className="feature">
            <div className="feature-icon">🔍</div>
            <h3>Search 300k+ Foods</h3>
            <p>Access the comprehensive USDA food database with detailed nutritional information</p>
          </div>

          <div className="feature">
            <div className="feature-icon">📊</div>
            <h3>Track Your Meals</h3>
            <p>Plan your daily meals and track if you're meeting your calorie and macro goals</p>
          </div>

          <div className="feature">
            <div className="feature-icon">💾</div>
            <h3>Save Your Progress</h3>
            <p>Save meal plans and track your nutrition history over time</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;

import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Home.css';

function Home() {
  const { user } = useAuth();

  return (
    <div className="home">
      {/* Navigation */}
      <nav className="nav">
        <div className="nav-container">
          <Link to="/" className="nav-logo">
            <span className="logo-icon">🍽️</span>
            <span className="logo-text">Meal Master</span>
          </Link>
          
          <div className="nav-links">
            <a href="#features" className="nav-link">Features</a>
            <a href="#how-it-works" className="nav-link">How It Works</a>
          </div>
          
          <div className="nav-actions">
            {user ? (
              <Link to="/dashboard" className="btn btn-primary">
                Go to Dashboard
                <span className="btn-arrow">→</span>
              </Link>
            ) : (
              <>
                <Link to="/login" className="btn btn-ghost">Sign In</Link>
                <Link to="/signup" className="btn btn-primary">
                  Start Free
                  <span className="btn-arrow">→</span>
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-glow hero-glow-1"></div>
        <div className="hero-glow hero-glow-2"></div>
        <div className="hero-content">
          <h1 className="hero-title">
            Master Your
            <br />
            <span className="hero-title-accent">Nutrition</span>
          </h1>
          <p className="hero-subtitle">
            Calculate your daily calorie needs, search from 300,000+ foods,
            and track your nutrition goals with precision.
          </p>
          <div className="hero-actions">
            <Link to="/signup" className="btn btn-primary btn-lg">
              Get Started Free
              <span className="btn-arrow">→</span>
            </Link>
            <a href="#how-it-works" className="btn btn-secondary btn-lg">
              See How It Works
            </a>
          </div>
          
          {/* Stats */}
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-value">300K+</span>
              <span className="stat-label">Foods in Database</span>
            </div>
            <div className="stat-divider"></div>
            <div className="stat">
              <span className="stat-value">USDA</span>
              <span className="stat-label">Verified Data</span>
            </div>
            <div className="stat-divider"></div>
            <div className="stat">
              <span className="stat-value">100%</span>
              <span className="stat-label">Free to Use</span>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works" id="how-it-works">
        <div className="section-container">
          <div className="section-header">
            <span className="section-tag">Simple Process</span>
            <h2 className="section-title">How it works.</h2>
            <p className="section-subtitle">
              Three steps to your perfect meal plan. It's really that easy.
            </p>
          </div>
          
          <div className="steps-grid">
            <div className="step-card">
              <div className="step-number">01</div>
              <div className="step-icon">🎯</div>
              <h3 className="step-title">Calculate Your TDEE</h3>
              <p className="step-description">
                Enter your stats and we'll calculate your Total Daily Energy Expenditure 
                using the scientifically-backed Mifflin-St Jeor equation.
              </p>
            </div>
            
            <div className="step-card">
              <div className="step-number">02</div>
              <div className="step-icon">🔍</div>
              <h3 className="step-title">Search & Add Foods</h3>
              <p className="step-description">
                Search our database of 300,000+ foods from USDA. Get detailed 
                nutritional info for each item and add them to your meal plan.
              </p>
            </div>
            
            <div className="step-card">
              <div className="step-number">03</div>
              <div className="step-icon">📊</div>
              <h3 className="step-title">Track Your Progress</h3>
              <p className="step-description">
                Monitor your daily intake against your goals. Track calories, 
                protein, carbs, and fats in real-time.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features" id="features">
        <div className="section-container">
          <div className="section-header">
            <span className="section-tag">Features</span>
            <h2 className="section-title">Why Choose Meal Master?</h2>
            <p className="section-subtitle">
              Everything you need to master your nutrition in one place.
            </p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card feature-card-large">
              <div className="feature-icon-wrapper">
                <span className="feature-icon">🧮</span>
              </div>
              <h3 className="feature-title">Precision TDEE Calculator</h3>
              <p className="feature-description">
                Calculate your exact daily calorie needs based on your weight, height, 
                age, gender, and activity level using the Mifflin-St Jeor equation – 
                the gold standard in metabolic rate calculation.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <span className="feature-icon">🔍</span>
              </div>
              <h3 className="feature-title">USDA Food Database</h3>
              <p className="feature-description">
                Search 300,000+ foods with verified nutritional data directly 
                from the USDA FoodData Central.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <span className="feature-icon">📋</span>
              </div>
              <h3 className="feature-title">Daily Meal Plans</h3>
              <p className="feature-description">
                Create and manage your daily meal plans with easy food tracking 
                and automatic calorie counting.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <span className="feature-icon">📊</span>
              </div>
              <h3 className="feature-title">Macro Tracking</h3>
              <p className="feature-description">
                Track protein, carbs, and fats alongside calories for complete 
                nutritional awareness.
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-wrapper">
                <span className="feature-icon">💾</span>
              </div>
              <h3 className="feature-title">Save Your Progress</h3>
              <p className="feature-description">
                Your meal plans and profile are saved securely so you can 
                track your nutrition journey over time.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-container">
          <div className="cta-glow"></div>
          <h2 className="cta-title">Ready to get started?</h2>
          <p className="cta-subtitle">
            Join thousands of users who are already mastering their nutrition.
          </p>
          <div className="cta-actions">
            <Link to="/signup" className="btn btn-primary btn-lg">
              Create Your Free Account
              <span className="btn-arrow">→</span>
            </Link>
          </div>
          <p className="cta-note">
            Already have an account? <Link to="/login" className="cta-link">Sign in</Link>
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-container">
          <div className="footer-brand">
            <span className="logo-icon">🍽️</span>
            <span className="logo-text">Meal Master</span>
            <p className="footer-tagline">Smart nutrition planning for everyone.</p>
          </div>
          
          <div className="footer-links">
            <div className="footer-column">
              <h4>Product</h4>
              <a href="#features">Features</a>
              <a href="#how-it-works">How It Works</a>
            </div>
            <div className="footer-column">
              <h4>Account</h4>
              <Link to="/login">Sign In</Link>
              <Link to="/signup">Get Started</Link>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>© 2024 Meal Master. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default Home;

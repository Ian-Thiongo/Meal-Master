import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Profile.css';

function Profile() {
  const { user, updateProfile, logout } = useAuth();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    email: user?.email || '',
    weight: user?.weight_kg || '',
    height: user?.height_cm || '',
    age: user?.age || '',
    gender: user?.gender || 'male',
    activity: user?.activity_level || 'moderately_active',
    isVegetarian: user?.is_vegetarian || false,
    isVegan: user?.is_vegan || false
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const { name, type, value, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const updates = {};
      
      if (formData.email !== user.email) updates.email = formData.email;
      if (formData.weight) updates.weight = parseFloat(formData.weight);
      if (formData.height) updates.height = parseFloat(formData.height);
      if (formData.age) updates.age = parseInt(formData.age);
      if (formData.gender) updates.gender = formData.gender;
      if (formData.activity) updates.activity = formData.activity;
      updates.is_vegetarian = formData.isVegetarian;
      updates.is_vegan = formData.isVegan;

      await updateProfile(updates);
      setSuccess('Profile updated successfully!');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="profile-page">
      <nav className="profile-nav">
        <h1>Meal Master</h1>
        <div className="nav-actions">
          <button onClick={() => navigate('/dashboard')} className="back-btn">
            ← Dashboard
          </button>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </nav>

      <div className="profile-content">
        <div className="profile-card">
          <div className="profile-header">
            <div className="avatar">
              {user?.username?.charAt(0).toUpperCase()}
            </div>
            <div className="profile-info">
              <h2>{user?.username}</h2>
              <p>{user?.email}</p>
              {user?.tdee && (
                <span className="tdee-badge">Daily Target: {Math.round(user.tdee)} kcal</span>
              )}
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          <form onSubmit={handleSubmit}>
            <h3>📧 Account Information</h3>
            
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                disabled={loading}
              />
            </div>

            <h3>📊 Physical Data</h3>
            <p className="section-desc">Used to calculate your daily calorie target (TDEE)</p>

            <div className="form-row">
              <div className="form-group">
                <label>Weight (kg)</label>
                <input
                  type="number"
                  name="weight"
                  value={formData.weight}
                  onChange={handleChange}
                  placeholder="e.g., 70"
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label>Height (cm)</label>
                <input
                  type="number"
                  name="height"
                  value={formData.height}
                  onChange={handleChange}
                  placeholder="e.g., 175"
                  disabled={loading}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Age</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  placeholder="e.g., 25"
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label>Gender</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  disabled={loading}
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Activity Level</label>
              <select
                name="activity"
                value={formData.activity}
                onChange={handleChange}
                disabled={loading}
              >
                <option value="sedentary">Sedentary (little/no exercise)</option>
                <option value="lightly_active">Lightly Active (1-3 days/week)</option>
                <option value="moderately_active">Moderately Active (3-5 days/week)</option>
                <option value="very_active">Very Active (6-7 days/week)</option>
                <option value="extra_active">Extra Active (very hard exercise)</option>
              </select>
            </div>

            <h3>🥗 Dietary Preference <span className="optional-tag">Optional</span></h3>
            <p className="section-desc">Let us know your dietary preferences for personalized recommendations</p>

            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="isVegetarian"
                  checked={formData.isVegetarian}
                  onChange={handleChange}
                  disabled={loading}
                />
                <span className="checkbox-text">I'm vegetarian 🥬</span>
              </label>
            </div>

            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="isVegan"
                  checked={formData.isVegan}
                  onChange={handleChange}
                  disabled={loading}
                />
                <span className="checkbox-text">I'm vegan 🌱</span>
              </label>
            </div>

            <button type="submit" className="save-btn" disabled={loading}>
              {loading ? 'Saving...' : 'Save Changes'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Profile;




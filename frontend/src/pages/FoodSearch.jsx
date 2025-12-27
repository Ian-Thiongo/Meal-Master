import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { API_URL } from '../config';
import './FoodSearch.css';

function FoodSearch() {
  const { token } = useAuth();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [totalResults, setTotalResults] = useState(0);
  const [todaysPlan, setTodaysPlan] = useState(null);
  const [addingFood, setAddingFood] = useState(null);
  const [servings, setServings] = useState({});
  const [successMessage, setSuccessMessage] = useState('');

  // Load today's meal plan on mount
  useEffect(() => {
    fetchTodaysPlan();
  }, []);

  const fetchTodaysPlan = async () => {
    try {
      const response = await fetch(`${API_URL}/api/meals/plans/today`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setTodaysPlan(data);
      }
    } catch (err) {
      console.error('Error fetching today\'s plan:', err);
    }
  };

  const searchFoods = async (e) => {
    e.preventDefault();
    
    if (query.length < 2) {
      setError('Please enter at least 2 characters');
      return;
    }

    setLoading(true);
    setError('');
    setSuccessMessage('');

    try {
      const response = await fetch(
        `${API_URL}/api/food/search?q=${encodeURIComponent(query)}&limit=20`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data = await response.json();
      setResults(data.foods);
      setTotalResults(data.total_results);
      
      // Initialize servings for all results
      const initialServings = {};
      data.foods.forEach(food => {
        initialServings[food.fdc_id] = 1;
      });
      setServings(initialServings);
    } catch (err) {
      setError('Failed to search foods. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const addToMeal = async (food) => {
    if (!todaysPlan) {
      setError('Could not load meal plan. Please refresh the page.');
      return;
    }

    setAddingFood(food.fdc_id);
    setError('');
    setSuccessMessage('');

    try {
      const response = await fetch(
        `${API_URL}/api/meals/plans/${todaysPlan.id}/meals`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            food_name: food.name,
            fdc_id: food.fdc_id,
            servings: servings[food.fdc_id] || 1,
            calories: food.calories,
            protein: food.protein,
            carbs: food.carbs,
            fat: food.fat
          })
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to add food');
      }

      const data = await response.json();
      setTodaysPlan(data.meal_plan);
      setSuccessMessage(`Added ${food.name} to your meal plan!`);
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err) {
      setError(err.message);
      console.error(err);
    } finally {
      setAddingFood(null);
    }
  };

  const removeMeal = async (mealId) => {
    if (!todaysPlan) return;

    try {
      const response = await fetch(
        `${API_URL}/api/meals/plans/${todaysPlan.id}/meals/${mealId}`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      if (response.ok) {
        const data = await response.json();
        setTodaysPlan(data.meal_plan);
        setSuccessMessage('Meal removed!');
        setTimeout(() => setSuccessMessage(''), 3000);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleServingsChange = (fdcId, value) => {
    setServings(prev => ({
      ...prev,
      [fdcId]: Math.max(0.1, parseFloat(value) || 1)
    }));
  };

  return (
    <div className="food-search">
      <div className="search-section">
        <h2>🔍 Search Foods</h2>
        <p className="subtitle">Search from 300,000+ foods in the USDA database</p>

        <form onSubmit={searchFoods} className="search-form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for foods (e.g., chicken, rice, apple)"
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>

        {error && <div className="error-message">{error}</div>}
        {successMessage && <div className="success-message">{successMessage}</div>}

        {totalResults > 0 && (
          <p className="results-count">
            Found {totalResults.toLocaleString()} results for "{query}"
          </p>
        )}

        <div className="food-results">
          {results.map((food) => (
            <div key={food.fdc_id} className="food-card">
              <div className="food-header">
                <h3>{food.name}</h3>
                <span className="food-brand">{food.brand}</span>
              </div>
              <div className="food-category">{food.category}</div>
              <div className="food-nutrients">
                <div className="nutrient calories">
                  <span className="value">{food.calories}</span>
                  <span className="label">kcal</span>
                </div>
                <div className="nutrient protein">
                  <span className="value">{food.protein}g</span>
                  <span className="label">Protein</span>
                </div>
                <div className="nutrient carbs">
                  <span className="value">{food.carbs}g</span>
                  <span className="label">Carbs</span>
                </div>
                <div className="nutrient fat">
                  <span className="value">{food.fat}g</span>
                  <span className="label">Fat</span>
                </div>
              </div>
              <div className="food-serving">
                Serving: {food.serving_size} {food.serving_unit}
              </div>
              <div className="add-section">
                <div className="servings-input">
                  <label>Servings:</label>
                  <input
                    type="number"
                    min="0.1"
                    step="0.1"
                    value={servings[food.fdc_id] || 1}
                    onChange={(e) => handleServingsChange(food.fdc_id, e.target.value)}
                  />
                </div>
                <button 
                  className="add-btn"
                  onClick={() => addToMeal(food)}
                  disabled={addingFood === food.fdc_id}
                >
                  {addingFood === food.fdc_id ? 'Adding...' : '+ Add to Meal'}
                </button>
              </div>
            </div>
          ))}
        </div>

        {results.length === 0 && !loading && query && (
          <p className="no-results">No results found. Try a different search term.</p>
        )}
      </div>

      {/* Today's Meal Plan Sidebar */}
      <div className="meal-plan-sidebar">
        <h3>📋 Today's Meals</h3>
        {todaysPlan && (
          <>
            <div className="plan-summary">
              <div className="calories-progress">
                <span className="consumed">{todaysPlan.total_calories || 0}</span>
                <span className="divider">/</span>
                <span className="target">{Math.round(todaysPlan.tdee_target)} kcal</span>
              </div>
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ 
                    width: `${Math.min(100, ((todaysPlan.total_calories || 0) / todaysPlan.tdee_target) * 100)}%`,
                    backgroundColor: (todaysPlan.total_calories || 0) > todaysPlan.tdee_target ? '#f44336' : '#4caf50'
                  }}
                />
              </div>
              <p className="remaining">
                {(todaysPlan.tdee_target - (todaysPlan.total_calories || 0)) > 0 
                  ? `${Math.round(todaysPlan.tdee_target - (todaysPlan.total_calories || 0))} kcal remaining`
                  : `${Math.abs(Math.round(todaysPlan.tdee_target - (todaysPlan.total_calories || 0)))} kcal over target`
                }
              </p>
            </div>

            <div className="meals-list">
              {todaysPlan.meals && todaysPlan.meals.length > 0 ? (
                todaysPlan.meals.map((meal) => (
                  <div key={meal.id} className="meal-item">
                    <div className="meal-info">
                      <span className="meal-name">{meal.food_name}</span>
                      <span className="meal-details">
                        {meal.servings} serving{meal.servings !== 1 ? 's' : ''} • {Math.round(meal.calories)} kcal
                      </span>
                    </div>
                    <button 
                      className="remove-btn"
                      onClick={() => removeMeal(meal.id)}
                      title="Remove"
                    >
                      ×
                    </button>
                  </div>
                ))
              ) : (
                <p className="no-meals">No meals added yet. Search and add some foods!</p>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default FoodSearch;

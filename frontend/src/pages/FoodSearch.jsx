import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './FoodSearch.css';

function FoodSearch() {
  const { token } = useAuth();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [totalResults, setTotalResults] = useState(0);

  const searchFoods = async (e) => {
    e.preventDefault();
    
    if (query.length < 2) {
      setError('Please enter at least 2 characters');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/food/search?q=${encodeURIComponent(query)}&limit=20`,
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
    } catch (err) {
      setError('Failed to search foods. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="food-search">
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
            <button className="add-btn">+ Add to Meal</button>
          </div>
        ))}
      </div>

      {results.length === 0 && !loading && query && (
        <p className="no-results">No results found. Try a different search term.</p>
      )}
    </div>
  );
}

export default FoodSearch;
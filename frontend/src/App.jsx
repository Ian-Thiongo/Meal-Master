import { useState } from 'react';
import './App.css';

function App() {
  // State for form fields
  const [weight, setWeight] = useState('');
  const [height, setHeight] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('male');
  const [activity, setActivity] = useState('sedentary');
  const [tdee, setTdee] = useState(null);

  // Function to handle form submit
  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevent page reload
    // Prepare the data as JSON
  const formData = {
    weight: parseFloat(weight),  // Convert string to number
    height: parseFloat(height),
    age: parseFloat(age),
    gender,
    activity
  };

  // Check if numbers are valid (basic validation)
  if (isNaN(formData.weight) || isNaN(formData.height) || isNaN(formData.age)) {
    alert('Please enter valid numbers for weight, height, and age!');
    return;  // Stop if invalid
  }

  // Send to backend
  try {
    const response = await fetch('http://127.0.0.1:5000/api/calculate_tdee', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });

    // Check if response is good
    if (!response.ok) {
      throw new Error('API error: ' + response.status);
    }

    const data = await response.json();
    setTdee(data.tdee);  // Update state with TDEE from backend
  } catch (error) {
    console.error(error);
    alert('Error calculating TDEE. Check console for details.');
  }
    // TODO: Call the backend API with form data
    // Hint: Use fetch like in the test button, but with form values
  };

  return (
    <div className="App">
      <h1>Meal Master - Calculate Your TDEE</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Weight (kg):
          <input
            type="number"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            required
          />
        </label>
        <br />
        <label>
          Height (cm):
          <input
            type="number"
            value={height}
            onChange={(e) => setHeight(e.target.value)}
            required
          />
        </label>
        <br />
        <label>
          Age:
          <input
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            required
          />
        </label>
        <br />
        <label>
          Gender:
          <select value={gender} onChange={(e) => setGender(e.target.value)}>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </label>
        <br />
        <label>
          Activity Level:
          <select value={activity} onChange={(e) => setActivity(e.target.value)}>
            <option value="sedentary">Sedentary</option>
            <option value="lightly_active">Lightly Active</option>
            <option value="moderately_active">Moderately Active</option>
            <option value="very_active">Very Active</option>
            <option value="extra_active">Extra Active</option>
          </select>
        </label>
        <br />
        <button type="submit">Calculate TDEE</button>
      </form>

      {tdee && <h2>Your TDEE: {Math.round(tdee)} kcal/day</h2>}
    </div>
  );
}

export default App;
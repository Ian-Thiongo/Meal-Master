# 🍽️ Meal Master

A full-stack meal planning and calorie tracking application that helps users calculate their daily calorie needs, search for foods, and track their nutrition goals.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)
![React](https://img.shields.io/badge/react-19-blue.svg)

## ✨ Features

- **TDEE Calculator** - Calculate your Total Daily Energy Expenditure using the Mifflin-St Jeor equation
- **Food Search** - Search from 300,000+ foods via the USDA FoodData Central API
- **Meal Planning** - Create and manage daily meal plans
- **Nutrition Tracking** - Track calories, protein, carbs, and fats
- **User Authentication** - Secure JWT-based authentication
- **Profile Management** - Update your physical data and recalculate your calorie targets

## 🏗️ Tech Stack

### Backend
- **Flask 3.1** - Python web framework
- **Flask-SQLAlchemy** - ORM with SQLite database
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **USDA FoodData Central API** - Food nutrition data

### Frontend
- **React 19** - UI library
- **React Router 7** - Client-side routing
- **Vite 7** - Build tool & dev server
- **CSS** - Custom styling

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- USDA API Key (get one free at [fdc.nal.usda.gov](https://fdc.nal.usda.gov/api-key-signup.html))

### Backend Setup

1. Navigate to the project root and create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `backend/` directory:
   ```env
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key
   USDA_API_KEY=your-usda-api-key
   ```

4. Start the backend server:
   ```bash
   cd backend
   python app.py
   ```
   
   The API will be available at `http://127.0.0.1:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   
   The app will be available at `http://localhost:5173`

## 📁 Project Structure

```
Meal-Master/
├── backend/                 # Flask REST API
│   ├── app.py              # Application factory
│   ├── auth.py             # Authentication routes
│   ├── food_api.py         # USDA API integration
│   ├── meals.py            # Meal plan routes
│   ├── models.py           # Database models
│   ├── calculations.py     # BMR/TDEE calculations
│   └── config.py           # Configuration
│
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── contexts/       # React contexts (Auth)
│   │   ├── pages/          # Page components
│   │   └── config.js       # API configuration
│   └── package.json
│
├── src/                    # Legacy CLI modules
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
└── README.md
```

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/signup` | Create new user account |
| POST | `/api/login` | Login and get JWT token |
| GET | `/api/profile` | Get user profile |
| PUT | `/api/profile` | Update user profile |

### Food Search
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/food/search?q=query` | Search for foods |
| GET | `/api/food/details/:fdc_id` | Get food details |
| GET | `/api/food/recommendations` | Get personalized recommendations |

### Meal Plans
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/meals/plans` | Get all meal plans |
| GET | `/api/meals/plans/today` | Get/create today's plan |
| GET | `/api/meals/plans/:id` | Get specific meal plan |
| POST | `/api/meals/plans/:id/meals` | Add meal to plan |
| DELETE | `/api/meals/plans/:id/meals/:meal_id` | Remove meal |
| DELETE | `/api/meals/plans/:id` | Delete meal plan |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | API health check |
| POST | `/api/calculate_tdee` | Calculate TDEE |

## 🧮 TDEE Calculation

The app uses the **Mifflin-St Jeor equation** to calculate Basal Metabolic Rate (BMR):

- **Men**: BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age) + 5
- **Women**: BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age) - 161

Then multiplies by an activity factor:

| Activity Level | Multiplier |
|---------------|------------|
| Sedentary | 1.2 |
| Lightly Active | 1.375 |
| Moderately Active | 1.55 |
| Very Active | 1.725 |
| Extra Active | 1.9 |

## 🖥️ CLI Version

A command-line version is also available:

```bash
python main.py
```

This provides a text-based interface for:
- Calculating TDEE
- Searching foods
- Building meal plans
- Saving/loading meal plans

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [USDA FoodData Central](https://fdc.nal.usda.gov/) for the comprehensive food database
- Mifflin-St Jeor equation for BMR calculation


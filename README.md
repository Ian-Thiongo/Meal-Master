# 🍽️ Meal Master

A modern, full-stack nutrition tracking application with smart meal recommendations and personalized calorie goals.

---

## ✨ Features

### 🔐 Authentication
- **Email + Password Signup** - 3-step verification with OTP codes
- **Google OAuth** - One-click login with Google
- **Email Verification** - 6-digit codes sent via email (10 min expiry)
- **Forgot Password** - Reset password via email verification
- **Password Visibility** - Eye toggle to show/hide passwords
- **JWT Sessions** - Secure token-based auth (24hr expiry)

### 👤 User Profile
- Track **weight, height, age, gender**
- **Activity Level** - 5 levels from sedentary to extra active
- **Auto TDEE Calculation** - Personalized daily calorie target
- **Dietary Preferences** - Vegetarian 🥬 and Vegan 🌱 options

### 🍳 Smart Meal Recommendations
- **TDEE-Balanced** - Breakfast (25%), Lunch (35%), Dinner (30%)
- **Dietary-Aware** - Different suggestions for vegetarian/vegan/regular
- **Time-Aware Prompts** - Greetings based on time of day
- **Daily Progress** - Visual progress bar for calorie tracking

###  Food Database
- **USDA Database** - Access to 300,000+ foods
- **Nutritional Info** - Calories, protein, carbs, fats
- **Meal Logging** - Track daily food intake

###  Premium UI
- Modern, minimalist SaaS design
- Syne + Outfit typography
- Purple-blue gradient accents
- Responsive (desktop + mobile)
- Smooth animations

---

##  Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, Vite |
| Styling | Vanilla CSS |
| Backend | Flask (Python) |
| Database | SQLite + SQLAlchemy |
| Auth | JWT, Google OAuth |
| Email | SMTP (Gmail) |
| Food API | USDA FoodData Central |

---

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python3 app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
Create `backend/.env`:
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
USDA_API_KEY=your-usda-api-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

---

##  Project Structure

```
Meal-Master/
├── backend/
│   ├── app.py              # Flask entry point
│   ├── auth.py             # Auth endpoints
│   ├── food_api.py         # Food/meal endpoints
│   ├── email_service.py    # OTP email service
│   ├── models.py           # Database models
│   └── calculations.py     # TDEE calculations
│
├── frontend/
│   ├── src/
│   │   ├── pages/          # React pages
│   │   ├── contexts/       # Auth context
│   │   └── components/     # Reusable components
│   └── index.html
```

---

## 📝 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/send-code` | Send OTP to email |
| POST | `/api/verify-code` | Verify OTP code |
| POST | `/api/signup` | Create account |
| POST | `/api/login` | Login with email/password |
| POST | `/api/reset-password` | Reset password |
| GET | `/api/oauth/google/login` | Google OAuth |

### User
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profile` | Get user profile |
| PUT | `/api/profile` | Update profile |

### Food
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/food/search` | Search foods |
| GET | `/api/food/meal-plan-suggestions` | Get meal recommendations |
| GET | `/api/food/daily-status` | Get daily progress |

---

## 📄 License

MIT License

---

Built with ❤️ by Ian Thiongo

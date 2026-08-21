# Protein Tracker

A daily protein intake calculator and tracker with a web interface built with **Flask** and data persistence using **SQLite**.

The app calculates a personalized daily protein target based on the user's body weight and goal (maintenance, muscle gain, or fat loss), lets them log their intake meal by meal throughout the day, and keeps a complete history tracking with statistics, charts, and streaks. It supports multiple users, each with their own separate history stored in the same database.

It started as a simple Python terminal script, evolved into a basic web application, and eventually became this version with complete history tracking and meal-by-meal logging.

---

## Features

- 🎯 **Personalized daily target** based on body weight and goal
- 🍽️ **Meal-by-meal logging** (e.g., Breakfast → Eggs 18g, Yogurt 12g)
- 🔵 **Progress ring** showing how much protein is left to reach the daily target
- 🔁 **Automatic day rollover** — no manual reset needed
- 🔥 **Streaks** — current and longest streak of days hitting the target
- 📊 **Statistics & charts** — overall, 7-day, and 30-day averages, plus a 30-day bar chart with a target line
- 📅 **Day details** — click any date in the history to see that day's target, total consumed, status, and recorded meals
- 👥 **Multiple users** — switch between users at any time, with fully separate histories

---

## How It Works

1. On the home screen, select an existing user or create a new one by entering their name, weight, and goal.
2. The app calculates that user's daily protein target.
3. Throughout the day, record what you consumed per meal. The total daily intake is the sum of all recorded items.
4. A progress ring shows how much protein is left to reach the target, with a notification when it's reached.
5. At midnight, the day rolls over automatically — the previous day is saved to history with no action needed.
6. The **History** tab shows:
   - Current streak and longest streak (both reset correctly when a day is missed)
   - Overall, 7-day, and 30-day averages
   - A 30-day bar chart with each day's target plotted as a line
   - A table of all recorded days
7. Clicking any date opens that day's details — target, amount consumed, status, and detailed meals (when available).
8. Users can be switched at any time without mixing up histories.

---

## Getting Started

**Prerequisite:** Python 3 installed.

```bash
# clone the repository
git clone https://github.com/Arthur-Isidoro/Protein-Tracker.git
cd Protein-Tracker

# install dependencies
pip install -r requirements.txt

# create the database (only needs to be run once)
python database.py

# run the application
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

### Quick Test (seed data)

To try the app with pre-populated users and history — instead of creating everything from scratch or waiting for real days to pass — run:

```bash
python seed_teste.py
```

This creates three test users:

| User | Goal | Description |
|---|---|---|
| **Teste** | Muscle gain | 21 days of history with broken streaks and full meals (Breakfast, Lunch, Snack, Dinner) every day, including today |
| **Testestreak** | Maintenance | 10 consecutive days hitting the target, with full meals — good for seeing a long, continuous streak |
| **Testezerado** | — | Registered with no records — useful for testing empty-state screens |

The script is safe to run multiple times: it reuses existing test users and replaces each day's meals instead of duplicating them.

---

## Project Structure

```
Protein-Tracker/
├── app.py                  # Flask routes, target calculation logic, and user session
├── database.py              # database table creation and all SQLite queries
├── seed_teste.py            # optional script to generate test users with history and meals
├── requirements.txt         # project dependencies
├── protein_tracker.db       # SQLite database (generated locally, not included in the repo)
├── templates/
│   ├── cadastro.html        # registered users list + new user creation
│   ├── tracker.html         # daily meal tracking and target progress
│   ├── historico.html       # streaks, statistics, chart, and daily records table
│   └── detalhe_dia.html     # details of a specific day, including meals
└── static/
    └── style.css             # page styles
```

---

## Database

The app uses SQLite (`protein_tracker.db`) with three tables:

- **`usuarios`** — each user's name, goal, and minimum/maximum protein target.
- **`registros_diarios`** — one daily summary per user (total protein consumed, daily target, whether it was reached). Powers the history, streaks, and chart.
- **`itens_consumidos`** — each recorded meal item (meal, food, grams of protein) by user and date. Used to build the current day's tracker and to show detailed meals for past days. The total in `registros_diarios` is the sum of that day's items.

The `.db` file is **not** included in the repository (it's in `.gitignore`). Each person who clones the project creates their own local database by running `python database.py`.

---

## How the Protein Target Is Calculated

| Goal | Protein per kg of body weight |
|---|---|
| Maintenance | 1.6 g/kg |
| Muscle Gain | 1.8 – 2.2 g/kg |
| Fat Loss | 2.0 – 2.4 g/kg |

---

## Possible Next Steps

- Migrate from SQLite to MySQL
- Move the target calculation logic into its own module
- Implement real authentication (password-based login) instead of user selection
- Allow editing an existing meal entry instead of removing and re-adding it

---

## About

Personal project built to practice and apply Python backend development concepts. It started as a terminal script and evolved step by step into a full Flask + SQLite web application with multi-user support, persistent data, and detailed history tracking.

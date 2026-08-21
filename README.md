<h1>Protein Tracker</h1>

<p>
  A daily protein intake calculator and tracker with a web interface built with Flask
  and data persistence using SQLite.
</p>

<p>
  The project calculates a user's daily protein target based on their body weight and
  goal (maintenance, muscle gain, or fat loss), allows them to track their protein
  intake by meal throughout the day, keeps a history with statistics and charts, and
  supports multiple users stored in the same database.
</p>

<p>
  It started as a Python terminal script, evolved into a simple web application, and
  eventually became this version with a complete history and meal-by-meal tracking.
</p>

<h2>How It Works</h2>

<ol>
  <li>On the home screen, you can select an existing user or create a new one by entering their name, weight, and goal.</li>

  <li>The app calculates the user's daily protein target.</li>

  <li>
    Throughout the day, you can record what you consumed in each meal
    (e.g., "Breakfast" → Eggs 18g, Yogurt 12g).
    The total daily intake is calculated by adding all recorded items.
  </li>

  <li>
    A progress ring visually shows how much protein is left to reach the daily target,
    with an explicit notification when the target is reached.
  </li>

  <li>
    The day changes automatically: as soon as the date changes, the previous day's
    intake is saved to the history without requiring any manual action.
  </li>

  <li>
    The History tab displays:
    <ul>
      <li>
        The current streak of consecutive days reaching the target and the longest
        streak ever achieved. Both correctly reset when a day is missed.
      </li>
      <li>Statistics: overall average, 7-day average, and 30-day average.</li>
      <li>
        A bar chart showing the last 30 days, with a line representing each day's target.
      </li>
      <li>A table containing all recorded days.</li>
    </ul>
  </li>

  <li>
    Clicking on any date in the history shows that day's details
    (target, consumed amount, and status), as well as the detailed meals recorded
    for that day, when available.
  </li>

  <li>
    Users can be switched at any time, while keeping each user's history separate.
  </li>
</ol>

<h2>Running Locally</h2>

<p><strong>Prerequisite:</strong> Python 3 installed.</p>

<pre><code># clone the repository
git clone https://github.com/Arthur-Isidoro/Protein-Tracker.git
cd Protein-Tracker

# install dependencies
pip install -r requirements.txt

# create the database (only needs to be run once)
python database.py

# run the application
python app.py</code></pre>

<p>
  Then open <code>http://127.0.0.1:5000</code> in your browser.
</p>

<h3>Quick Test</h3>

<p>
  If you want to test the app with pre-populated users and history without having to
  create everything from scratch or wait for real days to pass, run:
</p>

<pre><code>python seed_teste.py</code></pre>

<p>This creates three test users:</p>

<ul>
  <li>
    <strong>Teste</strong> — muscle gain, 21 days of history with broken streaks and
    detailed meals (Breakfast, Lunch, Snack, Dinner) for every day, including today.
  </li>

  <li>
    <strong>Testestreak</strong> — maintenance, 10 consecutive days reaching the target,
    with detailed meals for every day, allowing you to see a long, continuous streak.
  </li>

  <li>
    <strong>Testezerado</strong> — registered user with no records, useful for testing
    empty-state screens.
  </li>
</ul>

<p>
  The script is safe to run multiple times. It reuses existing test users and replaces
  each day's meals instead of creating duplicates.
</p>

<h2>Project Structure</h2>

<pre><code>Protein-Tracker/
├── app.py                  # Flask routes, target calculation logic, and user session
├── database.py             # database table creation and all SQLite queries
├── seed_teste.py           # optional script to generate test users with history and complete meals
├── requirements.txt        # project dependencies
├── protein_tracker.db      # SQLite database (generated locally, not included in the repository)
├── templates/
│   ├── cadastro.html       # registered users list + new user creation
│   ├── tracker.html        # daily meal tracking and target progress
│   ├── historico.html      # streaks, statistics, chart, and daily records table
│   └── detalhe_dia.html    # details of a specific day, including meals
└── static/
    └── style.css           # page styles</code></pre>

<h2>Database</h2>

<p>
  The app uses SQLite (<code>protein_tracker.db</code>) with three tables:
</p>

<ul>
  <li>
    <strong>usuarios</strong> — stores each user's name, goal, and minimum/maximum
    protein target.
  </li>

  <li>
    <strong>registros_diarios</strong> — stores one daily summary per user:
    total protein consumed, daily target, and whether the target was reached.
    This table powers the history, streaks, and chart.
  </li>

  <li>
    <strong>itens_consumidos</strong> — stores each recorded meal item
    (meal, food, and grams of protein) by user and date. It is used to build the
    current day's tracker and display detailed meals for previous days in the history.
    The total in <code>registros_diarios</code> is calculated by summing the items
    recorded for that day.
  </li>
</ul>

<p>
  The <code>.db</code> file is not included in the repository (it is listed in
  <code>.gitignore</code>). Each person who clones the project creates their own
  local database by running <code>python database.py</code>.
</p>

<h2>How the Protein Target Is Calculated</h2>

<table>
  <thead>
    <tr>
      <th>Goal</th>
      <th>Protein per kg of body weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Maintenance</td>
      <td>1.6 g/kg</td>
    </tr>
    <tr>
      <td>Muscle Gain</td>
      <td>1.8 g/kg to 2.2 g/kg</td>
    </tr>
    <tr>
      <td>Fat Loss</td>
      <td>2.0 g/kg to 2.4 g/kg</td>
    </tr>
  </tbody>
</table>

<h2>Possible Next Steps</h2>

<ul>
  <li>Migrate from SQLite to MySQL.</li>
  <li>Move the target calculation logic into its own module.</li>
  <li>
    Implement real authentication (password-based login) instead of user selection.
  </li>
  <li>
    Allow users to edit an existing meal entry instead of having to remove and add it again.
  </li>
</ul>

<h2>About</h2>

<p>
  Personal project created to practice Python after completing an introductory
  programming course.
</p>

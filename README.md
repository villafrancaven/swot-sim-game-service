# swot-sim-game-service

This repository contains the backend service for the SWOT Simulation Game.

## 🛠️ Setup

### 1. Clone the Repository

Clone the repo and navigate into the project directory:

```bash
git clone https://github.com/villafrancaven/swot-sim-game-service.git
cd swot-sim-game-service
```

### 2. Create and Activate a Virtual Environment

Create a Python virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows
```

### 3. Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Ensure you have PostgreSQL installed and running. If you don’t have it, follow the [official PostgreSQL installation guide](https://www.postgresql.org/download/).

#### 4.1 Create a Database

Create a new database for the service:

```bash
psql -U postgres
CREATE DATABASE swot_sim_game;
```

#### 4.2 Set Up Database URL

In the project root directory, create a `.env` file and set the following environment variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/swot_sim_game
```

Replace `username` and `password` with your PostgreSQL credentials.

#### 4.3 Initialize and Migrate the Database

Use Flask Migrate to set up the database schema:

1. Initialize the migrations folder:

   ```bash
   flask db init
   ```

2. Create migration files:

   ```bash
   flask db migrate
   ```

3. Apply the migrations to the database:

   ```bash
   flask db upgrade
   ```

### 5. Run the App

Start the Flask app:

```bash
python run.py
```

The backend server should now be running and accessible at [http://localhost:5000](http://localhost:5000).

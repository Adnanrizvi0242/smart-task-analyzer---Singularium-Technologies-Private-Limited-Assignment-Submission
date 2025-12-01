Smart Task Analyzer — Singularium Technologies Assignment

An intelligent task-prioritization system built using Django (Backend) and Vanilla JavaScript (Frontend).
The system analyzes tasks, detects circular dependencies, calculates urgency using business-day logic, and ranks tasks using multiple sorting strategies such as Fastest First, High-Impact, Deadline-Driven, and Smart Balanced AI Scoring.

This project also includes:

Dependency graph visualization
Eisenhower matrix
Learning system (adaptive weight adjustment using user feedback)
Multiple scoring strategies
Circular dependency detection
Unit tests
Clean API design

Features
Core Features

Create and analyze multiple tasks
Automatic scoring based on:
    Urgency (business-days based)
    Importance
    Effort (lower effort = higher ranking)
    Dependency count
Circular dependency detection (DFS based)
Configurable scoring weights
Multiple prioritization strategies:
    Smart Balanced (AI-based scoring)
    Fastest Wins
    High Impact
    Deadline Driven

📁 Project Structure
    ![alt text](image.png)

⚙️ Setup Instructions
✔ 1. Clone the Repository
git clone https://github.com/Adnanrizvi0242/smart-task-analyzer---Singularium-Technologies-Private-Limited-Assignment-Submission.git
cd smart-task-analyzer---Singularium-Technologies-Private-Limited-Assignment-Submission

✔ 2. Create Virtual Environment
python -m venv venv

✔ 3. Activate Virtual Environment
venv\Scripts\activate

✔ 4. Install Dependencies
pip install -r requirements.txt

✔ 5. Run Database Migrations
python manage.py migrate

✔ 6. Create Initial ScoringConfig Row
python manage.py shell
>>> from tasks.models import ScoringConfig
>>> ScoringConfig.objects.get_or_create(id=1)
>>> exit()

✔ 7. Run Backend Server
python manage.py runserver

✔ 8. Open Frontend

Open the file:

frontend/index.html
(Run using Live Server or double-click to open in a browser.)

🧠 Algorithm Explanation (400 Words)

The Smart Task Analyzer uses a weighted scoring model to determine the optimal order in which tasks should be completed. The scoring consists of four major components: urgency, importance, effort, and dependency load.

Urgency is computed using a business-day difference between today and the task’s due date. Weekends and holidays do not count as active workdays. If a task is overdue, the urgency increases using a logarithmic scale, ensuring urgency grows reasonably with time. Tasks without due dates receive zero urgency.

Importance is a user-supplied integer describing the impact or value of completing a task. Higher importance directly correlates with higher scoring weight.

Effort works inversely: lower effort increases the score because shorter tasks allow fast productivity wins. Longer tasks reduce priority but do not eliminate them; the effect is moderated through weighted scoring.

Dependencies reduce the score if a task requires other tasks to be completed first. Tasks with multiple dependencies rank lower, encouraging completion of foundational tasks first.

These factors combine as:

score = w_u * urgency 
      + w_i * importance 
      - w_e * effort 
      - w_d * dependency_count


The user may modify these weights using API parameters or indirectly influence them via the feedback system. When a user marks a result as "helpful" or "not helpful", the algorithm adjusts weights using a small learning rate, gradually shaping the scoring engine in line with real usage patterns.

Four prioritization strategies are available.
Smart Balanced uses the scoring formula above.
Fastest Wins sorts tasks by effort.
High Impact sorts tasks by importance.
Deadline Driven sorts tasks by earliest upcoming due date.

Circular dependencies are detected using a depth-first search that identifies cycles within the dependency graph. If detected, the API rejects the input and returns the cycle path.

The frontend visualizes tasks using:

Dependency Graph (vis-network)

Eisenhower Matrix for Urgent × Important analysis

Dynamic cards with explanations and scores

Together, these systems create a robust, smart, and adaptive prioritization engine.

💡 Design Decisions

Django REST chosen for simplicity and clarity

Avoided overly complex ML for scoring (assignment scope)

Vanilla JS instead of React to meet requirements

Used vis-network for graph rendering due to minimal setup

Adaptive feedback learning provides smarter personalization

SQLite chosen for speed and zero-configuration

⏱ Time Breakdown
Task	Time
Backend API	2 hours
Scoring Engine	1.5 hours
Strategy System	30 min
Cycle Detection	20 min
Frontend UI	1.5 hours
Dependency Graph	40 min
Eisenhower Matrix	40 min
Learning System	1 hour
Testing + Debugging	1 hour
Total	~8 hours


🧪 Unit Tests Included

✔ Scoring algorithm test
✔ Dependency cycle detection test
✔ API response + ordering test

🎯 Future Improvements

User accounts + personalized scoring history
ML-based learning system
Calendar & email integrations
Drag-and-drop UI for tasks
Real-time collaboration

TECH STACK SUMMARY

Backend:
Python, Django, Django REST Framework, SQLite, CORS Headers

Frontend:
HTML, CSS, JavaScript, Chart.js

Architecture:
Strategy Pattern, Factory Pattern, DFS Cycle Detection, REST API

Tools:
VS Code, Git, GitHub, Live Server, Virtual Environment

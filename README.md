# Gym Management System (GymFit)

A secure, full-stack Flask web application engineered to streamline fitness center administrative operations. This repository showcases production-ready backend design patterns, relational database architecture, secure session-based authentication, interactive scheduling, and dynamic ledger billing.

---

## 🎯 Recruiter & Technical Highlights

This project was built to demonstrate key software engineering competencies, architectural best practices, and clean code principles. Key skills showcased include:

*   **Robust Backend Architecture:** Developed using **Flask**, utilizing session-based authentication, helper authorization logic, secure routing, and robust error handling.
*   **Relational Database Design & ORM:** Engineered database schemas in **Flask-SQLAlchemy** featuring complex relationships (`one-to-many`), cascade deletes (`delete-orphan`), unique constraints across multiple columns, and clean separation of models ([models.py](file:///C:/Users/soumy/OneDrive/Documents/program/myGYM/models.py)) and views ([app.py](file:///C:/Users/soumy/OneDrive/Documents/program/myGYM/app.py)).
*   **Security Best Practices:** Integrated secure credential storage using **salted password hashing** (`Werkzeug.security`), secure file upload filtering (`secure_filename`), and environment isolation (`python-dotenv`).
*   **Automated Billing & Ledger Logic:** Built dynamic payment status checks, calculating monthly subscription dues, grace periods, and tracking manual payments with database constraints ensuring ledger integrity.

---

## 🛠️ Tech Stack & Dependencies

*   **Core Backend:** Python 3.10+, Flask
*   **Database & ORM:** SQLite (Development) / MySQL (Production-ready configuration supported via environment variables), SQLAlchemy
*   **Security & Env:** Werkzeug, Python-dotenv
*   **Frontend:** HTML5, Jinja2 Templates, Vanilla CSS3 (responsive grid and flexbox layouts)

---

## 🌟 Key Features

### 1. Administrative Authentication & Security
*   Secure portal restricting access to authorized managers.
*   Salted and hashed password verification via `PBKDF2`.
*   Auto-generated seed admin account on first application start.

### 2. Comprehensive Member Directory (CRUD)
*   Detailed profiles tracking contact information, medical conditions, and physical metrics (weight/height).
*   Unique photo uploading utility incorporating secure filename generation and automatic old-file cleanup upon update/removal.

### 3. Tiered Subscription & Plan Builder
*   Admin capability to define and structure gym plans with custom durations and pricing tiers.
*   Automatic membership expiration calculator showing `Active` or `Expired` badges based on subscription start dates.

### 4. Interactive Workout Planner
*   Personalized weekly schedule grids (Monday to Sunday) linked to individual member fitness goals.
*   Quick editing interface allowing trainers to adjust workouts dynamically.

### 5. Dynamic Payment Ledger & Billing
*   Auto-populated payment tracking showing active subscription periods.
*   Manual payment recording for members who continue training after subscription expiration, supported by unique database indexing to prevent double billing.

---

## 📂 Project Architecture

```
myGYM/
│
├── static/                 # Static assets (stylesheets & uploaded member photos)
│   ├── style.css           # Premium, responsive dark-themed styling
│   └── uploads/            # Safely managed member images (UUID filename obfuscated)
│
├── templates/              # Jinja2 layout templates
│   ├── base.html           # Master template with flash notification support
│   ├── dashboard.html      # Overview panels of members & active subscription plans
│   ├── member_insight.html # Deep-dive member profile, workouts, and payment status
│   └── ...                 # Add/edit forms and billing interfaces
│
├── .env                    # Local environment secrets & DB configs (Ignored in Git)
├── .gitignore              # Strict ignore rules for environments, DBs, and system files
├── app.py                  # Routing, controllers, and core application configurations
├── models.py               # Declarative SQLAlchemy models (Admin, Member, Subscription, Payment)
├── requirements.txt        # Managed project dependencies
└── README.md               # Documentation
```

---

## 🚀 Installation & Local Setup

### Prerequisites
*   Python 3.8 or higher installed.

### 1. Clone the Repository
```bash
git clone https://github.com/soumya4531-svg/Gym-Management.git
cd Gym-Management
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Or activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=generate-a-secure-random-key-here
# Optional Production Database Connection (defaults to local SQLite gym.db)
# DATABASE_URI=mysql+pymysql://username:password@host/database_name
```

### 5. Run the Application
```bash
python app.py
```
*The app will automatically initialize the database schema and output credentials for the default admin account:*
*   **Username:** `admin`
*   **Password:** `admin123`
*Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.*

---

## 🔮 Future Improvements & Scaling Ideas
*   **API Layer:** Introduce RESTful API endpoints for integration with mobile apps.
*   **Live Dashboard Analytics:** Implement monthly revenue charts and membership growth graphs.
*   **External Integration:** Integrate with payment gateways like Stripe or PayPal for real-time customer invoice billing.
*   **Role-Based Access Control (RBAC):** Separate user roles for trainers, members, and root-administrators.

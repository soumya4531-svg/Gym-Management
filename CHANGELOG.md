# Gym Admin Platform - Change Log

This file tracks all development changes, features, and database migrations applied to the Gym Admin Platform project.

---

## [2026-05-27] - Database Migrations & Advanced Profile Management

### 1. Cleanup of Unused Setup Files
- **Removed** `db_setup.py` (which created MySQL databases using PyMySQL).
- **Cleaned** [requirements.txt](file:///c:/Users/soumy/OneDrive/Documents/program/myGYM/requirements.txt) to remove unused packages (`PyMySQL`, `cryptography`) since the application runs solely on SQLite.

### 2. Optional Fields & Schema Correction
- **Database Schema Correction**: Added missing `weight`, `height`, and `medical_condition` columns to the `Member` table in `gym.db` to fix SQLite operational errors.
- **Optional Form Inputs**: Modified [add_member](file:///c:/Users/soumy/OneDrive/Documents/program/myGYM/templates/add_member.html) so that `email`, `weight`, `height`, and `medical_condition` are fully optional rather than mandatory.

### 3. Profile Details Editor
- **Implemented** dedicated member details editing route `/edit_member/<id>` in [app.py](file:///c:/Users/soumy/OneDrive/Documents/program/myGYM/app.py).
- **Created** [edit_member.html](file:///c:/Users/soumy/OneDrive/Documents/program/myGYM/templates/edit_member.html) template which pre-fills existing values.
- **Photo Upload/Removal**: Supported replacement of member photos and explicit photo deletion from the server disk.

### 4. Subscription Payment Overview
- **Implemented** a dynamic, month-by-month billing checklist showing subscription months and extra months beyond the plan.
- **Created** [subscription_overview.html](file:///c:/Users/soumy/OneDrive/Documents/program/myGYM/templates/subscription_overview.html) to show paid/due statuses.
- **Range & Dates**: Always displays at least 12 months dynamically. Added custom payment dates for manual entries, while subscription-paid months automatically use the subscription start date.

### 5. Workout Routine & Fitness Goal Tracking
- **Database Schema Migration**: Added columns to the `Member` database table to track:
  - `fitness_goal` (e.g., Weight Loss, Weight Gain)
  - `workout_monday` through `workout_sunday`
- **UI Display**: Implemented a responsive weekly grid under the profile insight showing the workouts day-by-day or displaying "💤 Rest Day" as the default.
- **Separated Editors**: 
  - Personal Details are edited on `/edit_member/<id>` ([edit_member.html](file:///c:/Users/soumy/OneDrive/Documents/program/myGYM/templates/edit_member.html)).
  - Goals & Weekly Routines are edited on `/member/<id>/edit_workout` ([edit_workout.html](file:///c:/Users/soumy/OneDrive/Documents/program/myGYM/templates/edit_workout.html)).

---

## Database Schema (Current Status)

### Table: `member`
| Column | Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Unique Member identifier |
| `first_name` | VARCHAR(50) | First name (Required) |
| `last_name` | VARCHAR(50) | Last name (Required) |
| `email` | VARCHAR(120) | Optional email address |
| `phone` | VARCHAR(20) | Phone number (Required) |
| `photo_filename`| VARCHAR(255) | Uploaded profile image filename |
| `join_date` | DATETIME | Registration timestamp |
| `weight` | FLOAT | Optional weight in kg |
| `height` | FLOAT | Optional height in cm |
| `medical_condition`| TEXT | Optional medical conditions |
| `fitness_goal` | VARCHAR(100) | Optional health goal |
| `workout_monday` | VARCHAR(255) | Monday workout schedule (or NULL for Rest Day) |
| `workout_tuesday`| VARCHAR(255) | Tuesday workout schedule (or NULL for Rest Day) |
| `workout_wednesday`| VARCHAR(255)| Wednesday workout schedule (or NULL for Rest Day) |
| `workout_thursday`| VARCHAR(255)| Thursday workout schedule (or NULL for Rest Day) |
| `workout_friday` | VARCHAR(255) | Friday workout schedule (or NULL for Rest Day) |
| `workout_saturday`| VARCHAR(255)| Saturday workout schedule (or NULL for Rest Day) |
| `workout_sunday` | VARCHAR(255) | Sunday workout schedule (or NULL for Rest Day) |
| `subscription_id`| INTEGER (FK) | Assigned Subscription Plan ID |
| `subscription_start`| DATE | Start date of subscription plan |

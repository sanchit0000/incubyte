# Employee Salary API

A production-ready FastAPI application for managing employee records and calculating country-specific salary deductions.

## Features

- **Employee CRUD:** Full management of employee resources.
- **Salary Calculation:** Automated TDS deductions (10% for India, 12% for US).
- **Salary Metrics:** Aggregated data (Min, Max, Avg) by country and job title.
- **SQLite Integration:** Persistent storage using SQLAlchemy 2.0.

## How to Run

1. **Setup Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

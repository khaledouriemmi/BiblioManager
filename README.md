# BiblioManager

## Description
BiblioManager is a Flask-based web application (currently in French) backed by an SQL database. It allows you to:

- **Add and manage subscribers**   
- **Add and manage books**  
- **Create loans**: assign a book to a subscriber by selecting a start date and end date for the loan  

> ⚠️ The interface and messages are in French only; no English version is available yet.

## Configuration
Before running the app, open your Flask configuration (`app.py`) and update the database credentials:

## Running the App
**1/Install dependencies:**

pip install -r requirements.txt

**2/Initialize or migrate your database as needed.**

**3/Start the server:**
flask run

**4/Open ***http://127.0.0.1:5000/*** in your browser.**

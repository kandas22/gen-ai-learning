# Flask Sample Application

This is a simple **Flask** web application that demonstrates how to create basic routes, return JSON responses, and handle user input using both **URL** and **query parameters**.

---

## 🚀 What is Flask?

**Flask** is a lightweight and flexible web framework for Python.  
It allows developers to quickly build web applications, APIs, and services with minimal setup.

Flask provides:
- A simple way to define routes and handle requests.
- Built-in development server and debugger.
- Easy integration with databases and templates.
- Flexibility for both small and large projects.

Official documentation: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)

---

## 📁 Project Structure

flask_app/
│
├── app.py # Main Flask application file
├── requirements.txt # Python dependencies (Flask)
└── README.md # Documentation file


---

## ⚙️ Installation & Setup

### 1. Clone or download this repository

```bash
git clone https://github.com/yourusername/flask_app.git
cd flask_app

2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # For macOS/Linux
venv\Scripts\activate         # For Windows

3. Install dependencies
Create a requirements.txt file (if not present) with:
Flask==3.0.3
Then run:
pip install -r requirements.txt

▶️ Running the App
To start the Flask app, run:
 * python app.py


You should see output similar to:
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit

🌐 Available Routes
1. Root Route

URL: /
Method: GET
Description: Returns a welcome message.
Example:
http://127.0.0.1:5000/

Response:

Welcome to the Flask App!

2. Health Check Route

URL: /health
Method: GET
Description: Simple health check endpoint for monitoring or testing.
Example:
http://127.0.0.1:5000/health

Response (JSON):

{
  "status": "healthy"
}

3. User Greeting (URL Parameter)

URL: /user/<name>
Method: GET
Description: Takes a user's name directly in the URL and returns a personalized greeting.
Example:
http://127.0.0.1:5000/user/Alice

Response (JSON):

{
  "message": "Hello, Alice!"
}

4. User Greeting (Query Parameter)

URL: /user?name=<name>
Method: GET
Description: Accepts the user's name as a query parameter instead.
Example:
http://127.0.0.1:5000/user?name=Bob

Response (JSON):

{
  "message": "Hello, Bob!"
}


If no name is provided:

{
  "message": "Hello, Guest!"
}

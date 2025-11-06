from flask import Flask,jsonify
app = Flask(__name__)


@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/')
def home():
    return "Welcome to the Flask App!"

@app.route('/user/<name>')
def user(name):
    return jsonify({"message": f"Hello, {name}!"})

if __name__ == '__main__':
    app.run(debug=True)
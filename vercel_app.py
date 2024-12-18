from flask import Flask
from app import app as flask_app

app = flask_app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

from flask import Flask # type: ignore
from flask_pymongo import PyMongo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)

from routes.device_routes import device_bp
from routes.user_routes import user_bp
from routes.alert_routes import alert_bp

app.register_blueprint(device_bp, url_prefix='/api/devices')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(alert_bp, url_prefix='/api/alerts')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

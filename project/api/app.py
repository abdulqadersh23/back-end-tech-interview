from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask import Flask, render_template
import os


# routes
from routes.users import users_bp
from routes.devices import devices_bp
from routes.telemetry import telemetry_bp
from routes.auth import auth_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "..", "front-end")
)

# config
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

# init extensions
jwt = JWTManager(app)
CORS(app)

# register blueprints
app.register_blueprint(users_bp)
app.register_blueprint(devices_bp)
app.register_blueprint(telemetry_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
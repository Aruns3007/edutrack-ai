from flask import Flask, render_template
from extensions import db, bcrypt, login_manager
import os

app = Flask(__name__)

# --- 1. Configuration ---
app.config['SECRET_KEY'] = 'your_secret_key'
basedir = os.path.abspath(os.path.dirname(__file__))

# Database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')

# Folder path - placed in static so browser can view PDFs/images
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')

# --- 2. Initialize Extensions ---
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# --- 3. Login Manager Setup ---
from models.user_model import User

@login_manager.user_loader
def load_user(user_id):
    # UPDATED: Replaced legacy User.query.get() with modern db.session.get()
    # This fixes the LegacyAPIWarning in your logs.
    return db.session.get(User, int(user_id))

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# --- 4. Import Models (Required for db.create_all) ---
from models.attendance_model import Attendance
from models.notes_model import Notes
from models.timetable_model import Timetable

# --- 5. Register Blueprints ---
from routes.auth_routes import auth
from routes.dashboard_routes import dash
from routes.ai_routes import ai
from routes.notes_routes import learning
from routes.attendance_routes import att
from routes.timetable_routes import time_table 

app.register_blueprint(auth)
app.register_blueprint(dash)
app.register_blueprint(ai)
app.register_blueprint(learning)
app.register_blueprint(att)
app.register_blueprint(time_table) 

# --- 6. Home Route ---
@app.route('/')
def index():
    return render_template('index.html')

# --- 7. System Initialization ---
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(os.path.join(basedir, 'instance')):
    os.makedirs(os.path.join(basedir, 'instance'))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
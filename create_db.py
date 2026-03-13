from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# This line creates the actual file 'database.db' in your project folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Important: This allows the create_db script to find your models
from models.user_model import User
from models.attendance_model import Attendance
from models.notes_model import Notes
from models.timetable_model import Timetable

from app import app
from extensions import db
from models.user_model import User
from models.attendance_model import Attendance
from models.notes_model import Notes
from models.timetable_model import Timetable

with app.app_context():
    print("Creating database...")
    db.create_all()
    print("Success! database.db is ready.")
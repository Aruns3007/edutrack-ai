from app import app, db
import os

# This script manually wipes the old DB and creates a fresh one with your new columns
with app.app_context():
    print("Resetting database...")
    db.drop_all()  # Removes old tables
    db.create_all() # Creates new tables (including 'subject')
    print("Database recreated successfully!")
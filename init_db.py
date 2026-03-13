from app import app, db
import os

# Ensure the 'uploads' folder exists so the app doesn't crash later
if not os.path.exists('uploads'):
    os.makedirs('uploads')

with app.app_context():
    print("Resetting database tables...")
    # This deletes the old table (missing 'subject') and creates the new one
    db.drop_all() 
    db.create_all()
    print("Database is now synced with your model!")
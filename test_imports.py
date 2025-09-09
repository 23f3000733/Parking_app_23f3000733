#!/usr/bin/env python3

print("Testing imports...")

try:
    import flask
    print("✓ Flask imported successfully")
except ImportError as e:
    print(f"✗ Flask import failed: {e}")

try:
    from flask_sqlalchemy import SQLAlchemy
    print("✓ Flask-SQLAlchemy imported successfully")
except ImportError as e:
    print(f"✗ Flask-SQLAlchemy import failed: {e}")

try:
    from models import db
    print("✓ Models imported successfully")
except ImportError as e:
    print(f"✗ Models import failed: {e}")

try:
    from app import app
    print("✓ App imported successfully")
except ImportError as e:
    print(f"✗ App import failed: {e}")

print("\nCurrent working directory:", __import__('os').getcwd())
print("Python path:")
import sys
for path in sys.path:
    print(f"  {path}")

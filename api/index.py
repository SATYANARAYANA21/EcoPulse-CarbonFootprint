"""
Vercel serverless entry point for the EcoPulse FastAPI backend.
"""
import sys
import os

# Add parent directory and backend directory to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)
sys.path.insert(0, os.path.join(root_dir, "backend"))

os.environ.setdefault("USE_GEMINI", "false")
os.environ.setdefault("USE_FIRESTORE", "false")
os.environ.setdefault("USE_BIGQUERY", "false")
os.environ.setdefault("USE_PUBSUB", "false")
os.environ.setdefault("PROJECT_ID", "dummy-project")
os.environ.setdefault("REGION", "us-central1")
os.environ.setdefault("ENVIRONMENT", "production")
os.environ.setdefault("LOG_LEVEL", "INFO")

from backend.app.main import app  # noqa: F401, E402

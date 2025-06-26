import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin SDK
import os

cred_path = os.path.join(
    os.path.dirname(__file__), "credentials", "firebase-service-account.json"
)

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

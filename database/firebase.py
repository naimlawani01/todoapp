import json
import firebase_admin
from firebase_admin import credentials
import pyrebase 
import os

from dotenv import load_dotenv

load_dotenv()

config={
    "FIREBASE_SERVICE_ACCOUNT_KEY": os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY"),
    "FIREBASE_CONFIG": os.getenv("FIREBASE_CONFIG")
}
# Initialize Firebase Admin with the service account information
cred = credentials.Certificate("configs/todoapp-6c1f4-firebase-adminsdk-65ewn-ea2300eca5.json")
firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(json.loads(config['FIREBASE_CONFIG']))
db = firebase.database()
authSession = firebase.auth()

print(config["FIREBASE_SERVICE_ACCOUNT_KEY"])
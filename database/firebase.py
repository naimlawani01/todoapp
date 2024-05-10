# Importe le module firebase_admin nécessaire pour l'initialisation de Firebase
import firebase_admin
 
from firebase_admin import credentials
 
import pyrebase
import json
from dotenv import dotenv_values
 
config = dotenv_values(".env")
 
#from configs.firebase_config import firebase_config
 
if not firebase_admin._apps:
 
    # Charge les informations d'authentification
    cred = credentials.Certificate(json.loads( config['FIREBASE_SERVICE_ACCOUNT_KEY'], strict=False))
   
 
    # Initialise l'application Firebase
    firebase_admin.initialize_app(cred)
 
# Initialise l'application Firebase
firebase = pyrebase.initialize_app(json.loads(config['FIREBASE_CONFIG'], strict=False))
 
# Crée une instance de la base de données Firebase
db = firebase.database()
authStudent = firebase.auth()
authSession = firebase.auth()
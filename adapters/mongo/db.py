# Connexion MongoDB
from motor.motor_tornado import MotorClient
from config import settings

client = MotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

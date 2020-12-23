import os
from app import db
import config
from app.models import User, Object_ID
from datetime import datetime

USERS = []

OBJECTS = []

config.createTables()

print("Tables created")

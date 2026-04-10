#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from falsk_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
import os

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://millie:ciku2015@localhost/Library_Management_API'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


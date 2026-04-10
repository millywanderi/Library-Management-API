#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from falsk_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
import os

# Initialize Flask app
app = Flask(__name__)


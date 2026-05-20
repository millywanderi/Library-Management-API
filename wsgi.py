#!/usr/bin/env python3

from flask_app import create_app
from config import ProductionConfig

app = create_app(ProductionConfig)

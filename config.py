#!/usr/bin/env python3

import os

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI)
    CACHE_TYPE = "SimpleCache"

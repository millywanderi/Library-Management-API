#!/usr/bin/env python3

import os
from dotenv import load_dotenv

load_dotenv()


class developmentConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://millie:ciku2015@localhost/Library_Management_API"
    DEBUG = True
    CACHE_TYPE = "SimpleCache"


class TestingConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = "SimpleCache"

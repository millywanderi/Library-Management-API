#!/usr/bin/env python3

import os

class developmentConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://millie:ciku2015@localhost/Library_Management_API"
    Debug = True
    CACHE_TYPE = "SimpleCache"


class TestingConfig:
    Debug = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CACHE_TYPE = "SimpleCache"


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI)
    CACHE_TYPE = "SimpleCache"

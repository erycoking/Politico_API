import os

class configurations:
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(configurations):
    """Configurations for Development."""
    DEBUG = True


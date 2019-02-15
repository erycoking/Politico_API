"""Entry to the application"""
from politico.config import create_app

"""Initializing application"""
app = create_app()

"""Setting debug to true"""

if __name__ == '__main__':
    app.run()
from politico import create_app
import os

"""Entry to the application"""
"""Initializing application"""
config = os.getenv('FLASK_ENV')
app = create_app(config)

"""Setting debug to true"""
if __name__ == '__main__':
    app.run()

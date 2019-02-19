from politico import create_app
import os

"""Entry to the application"""
"""Initializing application"""
app = create_app(os.getenv('FLASK_ENV'))

"""Setting debug to true"""
if __name__ == '__main__':
    app.run()

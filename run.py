from politico import create_app
import os

"""Entry to the application"""
"""Initializing application"""
app = create_app('development')

"""Setting debug to true"""
if __name__ == '__main__':
    app.run()

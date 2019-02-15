import os

"""Entry to the application"""
from politico.config import create_app

"""Initializing application"""
app = create_app()

"""Setting debug to true"""
# app.run(host='0.0.0.0', port=5000, debug=True)
app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 9999)))
#!flask/bin/python
from app import app
from flask_script import Manager
manager = Manager(app)
manager.run()
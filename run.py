#!flask/bin/python
from app import app
from flask_script import Manager
app.run(debug = True)
#manager = Manager(app)
#manager.run()
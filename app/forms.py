from flask_wtf import Form
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Required

class SearchForm(Form):
    searchKey = StringField('searchKey', validators = [DataRequired()])
    
class RequestForm(Form):
    branch_request = StringField('branch', validators = [DataRequired()])
    year_request = StringField('year', validators = [DataRequired()])
    sub_request = StringField('sub', validators = [DataRequired()])

class UploadForm(Form):
    branch = StringField('branch', validators = [DataRequired()])
    year = StringField('year', validators = [DataRequired()])
    sub = StringField('sub', validators = [DataRequired()])
    paper = FileField('paper', validators = [Required()])
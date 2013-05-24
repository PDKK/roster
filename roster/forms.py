from flask.ext.wtf import Form
from wtforms import TextField,  BooleanField, IntegerField, FloatField, HiddenField
from wtforms.validators import Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from roster.models import Category

def category_factory():
    return Category.query

class EntryForm(Form):
    name = TextField('name')
    age = IntegerField('age', validators=[Optional()])
    club = TextField('club')
    category = QuerySelectField(query_factory=category_factory, get_label='name')
    time = FloatField('time', validators=[Optional()])
    history = TextField('history')

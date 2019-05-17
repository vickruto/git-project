# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,IntegerField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Workshop

class WorkshopForm(FlaskForm):
    """
    Form for admin to add or edit a workshop
    """
    
    workshop=StringField('Workshop',validators=[DataRequired()])
    date=StringField('Date',validators=[DataRequired()])
    #next line initially not there
    description = StringField('Description', validators=[DataRequired()])
    submit=SubmitField('Post')


class RoomForm(FlaskForm):
    """
    Form for admin to add or edit a room
    """
    room_no=StringField('Room NO',validators=[DataRequired()])
    capacity=StringField('Capacity',validators=[DataRequired()])
    submit=SubmitField('Post')


class RoomAssignWorkshopForm(FlaskForm):
    """
    Form for admin to assign rooms to workshops
    """
    Workshops=QuerySelectField(query_factory=lambda:Workshop.query.all(),
                                  get_label="workshop")
    workshop_id=IntegerField('Workshop ID(int)',validators=[DataRequired()])
    submit=SubmitField('Assign')

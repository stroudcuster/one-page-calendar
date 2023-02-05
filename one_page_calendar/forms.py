from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import NumberRange, DataRequired, Optional

import one_page_calendar.model as model


class CalendarFunctionForm(FlaskForm):
    """
    A FlaskForm class that allows the entry selection of a one_page_calender.model.Month value and one of the following:
    A one_page_calendar.Cardinal value and a one_page_calendar.Day value.  Along withe the selected Month value, this
    is used to determine the corresponding day(s) of the month.
    A day of the month int value, along with the selected Month value, this used is to determine the corresponding
    one_page_calendar.Day value

    """
    month_selection = SelectField(label='Month', coerce=int, validators=[DataRequired()],
                                  choices=[(month.value, month.name)
                                  for month in model.Month if month != model.Month.NoMonth])
    day_selection = SelectField(label='Day', coerce=int, validators=[Optional()],
                                choices=[(day.value, day.name) for day in model.Day])
    interval_selection = SelectField(label='Every', validators=[Optional()],
                                     choices=[(card.value, card.name) for card in model.Cardinal])
    day_of_month = IntegerField(label='Day of Month', validators=[Optional(), NumberRange(1, 31)])
    submit = SubmitField(label='Submit')

    def __init__(self, *args, **kwargs):
        """
        Creates an instance of CalendarFunctionForm

        :param args:
        :param kwargs:

        """

        super(CalendarFunctionForm, self).__init__(*args, **kwargs)

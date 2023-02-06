from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import NumberRange, DataRequired, Optional, ValidationError

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
                                choices=[(day.value, day.name) for day in model.Day] + [(0, 'None')],
                                default=0)
    interval_selection = SelectField(label='Every', validators=[Optional()],
                                     choices=[(card.value, card.name) for card in model.Cardinal] + [(0, 'None')],
                                     default=0)
    day_of_month = IntegerField(label='Day of Month', validators=[Optional(), NumberRange(1, 31)])
    submit = SubmitField(label='Submit')

    def __init__(self, *args, **kwargs):
        """
        Creates an instance of CalendarFunctionForm

        :param args:
        :param kwargs:

        """
        super(CalendarFunctionForm, self).__init__(*args, **kwargs)

    @staticmethod
    def validate_day_selection(form, field):
        """
        Validates the Day of the Week selection value to assure that if a Day was selected, a Day of the Month value
        was not entered and an Interval value was selected.

        :param form: the enclosing form instance
        :type form: one_page_calendar.forms.CalendarFunctonForm
        :param field: the day_selection instance
        :type field: SelectField
        :return: False

        """
        if field.data != 0:
            if form.day_of_month.data is not None and form.day_of_month.data != 0:
                raise ValidationError('Day of Week and Day of Month are mutually exclusive')
            if int(form.interval_selection.data) == 0:
                raise ValidationError('If you select a Day of the Week, you must select an Interval')
        else:
            if int(form.interval_selection.data) == 0 and \
                    (form.day_of_month.data is None or form.day_of_month.data == 0):
                raise ValidationError('You must either select an Interval and a Day of '
                                      'the Week or enter a Day of the Month.')
        return False

    @staticmethod
    def validate_interval_selection(form, field):
        """
        Validates the Interval selection to assure that if an Interval was selected, a Day of the Month value
        was not entered and a Day of the Week value was selected.

        :param form: the enclosing form instance
        :type form: one_page_calendar.forms.CalendarFunctonForm
        :param field: the interval_selection instance
        :type field: SelectField
        :return: False

        """
        if field.data.strip() != '0':
            if form.day_of_month.data is not None and form.day_of_month.data != 0:
                raise ValidationError('Interval and Day of Month are mutually exclusive.')
            if form.day_selection.data == 0:
                raise ValidationError('If you select an Interval you must select a Day of the Week')
        return False

    @staticmethod
    def validate_day_of_month(form, field):
        """
        Validates the Day of the Month value to assure that if a value was entered, neither a Day of the Week or
        Interval was selected, and the value entered if valid for the selected month

        :param form: the enclosing form instance
        :type form: one_page_calendar.forms.CalendarFunctonForm
        :param field: the day_of_month instance
        :type field: IntegerField
        :return: False

        """
        if field.data is not None and field.data != 0:
            if (interval_select := int(form.interval_selection.data)) != 0 or form.day_selection.data != 0:
                if form.day_selection.data != 0:
                    raise ValidationError('Day of Month and Day of Week are mutually exclusive.')
                if interval_select != 0:
                    raise ValidationError('Day of Month and Interval are mutually exclusive.')
            else:
                month = model.Month(form.month_selection.data)
                if field.data > model.max_dom[month]:
                    raise ValidationError(f'{field.data} is not a valid Day of Month for {month.name}.')
        return False

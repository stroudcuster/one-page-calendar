from flask import Flask, render_template
from wtforms import ValidationError

import one_page_calendar.model as model
import one_page_calendar.forms as forms
import one_page_calendar.utilities as util


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'AJF;AALJOIADSNA;FJKD'

calendars: dict[int, model.OnePageCal] = {}


@app.route('/calendar/<year_str>', methods=['GET'])
def calendar_get(year_str: str):
    """
    Decorated with @app.route('/calender/<year_str>, methods=['GET']).
    This method creates or retrieves a one_page_calendar.OnePageCal instance for the specified year and renders an
    HTML page that displays the calendar and a one_page_calendar.forms.CalendarFunctionForm using the template
    calendar-form.html

    :param year_str: the specified year in string form
    :type year_str: str
    :return: the rendered HTML page

    """
    year: int = int(year_str)
    form = forms.CalendarFunctionForm()
    if year in calendars:
        cal = calendars[year]
    else:
        cal = model.OnePageCalFactory.for_year(year)
        calendars[year] = cal
    return render_template('calendar-form.html', year=year,
                           month_rows=[row for row in cal.month_rows()],
                           dom_rows=[row for row in cal.dom_rows()],
                           dow_rows=[row for row in cal.dow_rows()],
                           form=form)


@app.route('/calendar/<year_str>', methods=['POST'])
def calendar_post(year_str):
    """
    Decorated with @app.route('/calender/<year_str>, methods=['POST']).
    This method handles the submit of the form rendered by the calendar_get method.  The Month, Cardinal, Day and
    day of month values are used to retrieve either the day(s) of the months corresponding to the Month, Cardinal
    and Day or the Day corresponding the Month and day of the month values. The results of this retrieval are
    rendered as an HTML page using the template calendar-result.html

    :param year_str: the specified year, carried over from the GET
    :return: the rendered HTML page

    """
    year = int(year_str)
    cal = calendars[year]
    form = forms.CalendarFunctionForm()
    sel_month = ''
    sel_month_col = 0
    sel_doms = []
    sel_dow = None
    result = ''
    if form.validate_on_submit():
        sel_month = model.Month(form.month_selection.data)
        for row in cal.month_rows():
            if sel_month in row:
                sel_month_col = [col for col in row].index(sel_month)
                break
        if form.day_of_month.data is None or form.day_of_month.data == 0:
            sel_dow = model.Day(form.day_selection.data)
            doms = cal.doms_for_dow(model.Month(form.month_selection.data), sel_dow)
            sel_doms = doms
            if int(form.interval_selection.data) == model.Cardinal.All.value:
                result = f'The {model.Day(form.day_selection.data).name}s ' \
                         f'in {model.Month(form.month_selection.data).name} ' \
                         f'are {",".join([util.ordinal(dom) for dom in doms if dom > 0])}.'

            else:
                sel_doms = [doms[int(form.interval_selection.data)-1]]
                result = f'The {model.Cardinal(int(form.interval_selection.data)).name} ' \
                         f'{model.Day(form.day_selection.data).name} ' \
                         f'of {model.Month(form.month_selection.data).name} is ' \
                         f'the {util.ordinal(sel_doms[0])}'
        else:
            sel_dow = cal.dow_for_dom(model.Month(form.month_selection.data), form.day_of_month.data)
            sel_doms = [form.day_of_month.data]
            result = f'{model.Month(form.month_selection.data).name} {util.ordinal(form.day_of_month.data)} is a ' \
                     f'{sel_dow.name}'
        return render_template('calendar-result.html', year=year,
                               month_rows=[row for row in cal.month_rows()],
                               dom_rows=[row for row in cal.dom_rows()],
                               dow_rows=[row for row in cal.dow_rows()],
                               sel_month=sel_month.name,
                               sel_month_col=sel_month_col,
                               sel_doms=sel_doms,
                               sel_dow=sel_dow.name,
                               result=result,
                               error=[])
    else:
        errors = [error[0] for error in form.errors.values()]
        return render_template('calendar-result.html', year=year,
                               month_rows=[row for row in cal.month_rows()],
                               dom_rows=[row for row in cal.dom_rows()],
                               dow_rows=[row for row in cal.dow_rows()],
                               sel_month='None',
                               sel_month_col=0,
                               sel_doms=[],
                               sel_dow='None',
                               result=' ',
                               errors=errors)







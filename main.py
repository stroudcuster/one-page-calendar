import one_page_calendar.model as model

if __name__ == '__main__':
    for year in range(2003, 2051):
        cal = model.OnePageCalFactory.for_year(year)
        x = cal.dow_for_dom(model.Month.February, 7)
        y = cal.doms_for_dow(model.Month.February, model.Day.Wednesday)
        print(f'{year} Feb 7th is {x.name} The Weds in Feb are {y}')
    """
    for month_row in cal.month_rows():
        print(month_row)
    for dom_row in cal.dom_rows():
        print(dom_row)
    for dow_row in cal.dow_rows():
        print(dow_row)
    """
    pass




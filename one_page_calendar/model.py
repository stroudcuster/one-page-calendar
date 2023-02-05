import calendar
from datetime import date
from enum import Enum, auto
from typing import Iterator

import numpy as np


class Day(Enum):
    """
    An Enum to represent the days of the week

    """
    Monday = auto()
    Tuesday = auto()
    Wednesday = auto()
    Thursday = auto()
    Friday = auto()
    Saturday = auto()
    Sunday = auto()


class Month(Enum):
    """
    An Enum to represent the months of the year, plus a NoMonth value

    """
    January = auto()
    February = auto()
    March = auto()
    April = auto()
    May = auto()
    June = auto()
    July = auto()
    August = auto()
    September = auto()
    October = auto()
    November = auto()
    December = auto()
    NoMonth = auto()


class Cardinal(Enum):
    """
    A Enum to represent the ordinals from First to Fourth, plus a value to represent All

    """
    First = auto()
    Second = auto()
    Third = auto()
    Fourth = auto()
    All = auto()


max_dom: dict[Month, int] = {
    Month.January: 31,
    Month.February: 28,
    Month.March: 31,
    Month.April: 30,
    Month.May: 31,
    Month.June: 30,
    Month.July: 31,
    Month.August: 31,
    Month.September: 30,
    Month.October: 31,
    Month.November:30,
    Month.December: 31
}


class OnePageCalBase:
    """
    This class provides methods that are used in the __init__ method of the OnePageCal class

    """
    dow_list: list[Day] = [Day.Monday, Day.Tuesday, Day.Wednesday, Day.Thursday, Day.Friday,
                           Day.Saturday, Day.Sunday]

    @staticmethod
    def build_dom_grid():
        """
        This method builds the Day of the Month grid as a numpy array of integers with a shape of (7, 5).  The series
        proceeds in a column-wise order

        :return: the Day of the Month grid
        :rtype: numpy.array

        """
        dom_lists: list[list[int]] = []
        for dom1 in range(1, 8):
            dom_list: list[int] = [0, 0, 0, 0, 0]
            for idx, dom2 in enumerate(range(dom1, 32, 7)):
                dom_list[idx] = dom2
            dom_lists.append(dom_list)
        doms: list[int] = []
        for dom_list in dom_lists:
            for dom in dom_list:
                doms.append(dom)
        dom_array = np.array(doms)
        return dom_array.reshape((7, 5))

    @staticmethod
    def build_dow_grid():
        """
        This method builds the Day of the Week grid as a numpy array of Day enums with a shape of (7,7).  The day
        sequence proceeds in a column-wise order.

        :return: the Day of the Week grid
        :rtype: numpy.array

        """
        dow_lists: list[list[Day]] = [[] for _ in range(0, 7)]
        dow_lists[0] = OnePageCalBase.dow_list
        for idx in range(1, 7):
            dow_lists[idx] = dow_lists[idx-1][1:7] + [dow_lists[idx-1][0]]
        dows: list[Day] = []
        for dow_list in dow_lists:
            for dow in dow_list:
                dows.append(dow)
        dow_array = np.array(dows)
        return dow_array.reshape((7, 7))


class OnePageCal:
    """
    This class implements a calendar that covers an entire year within a single concise representation, which consists
    of three grids: a Month grid, a Day of the Week grid, and a Day of the Month grid.  The latter two are invariant
    from year to year.  The month grid is built starting with the day of week of the January 1st for a given year.
    These grids are related as follows: the columns of the Month grid and the Day of the Week grid are aligned and the
    rows of the Day of the Month grid and the Day of the Week grid are aligned.  Each month is

    """
    dom_grid = OnePageCalBase.build_dom_grid()
    dow_grid = OnePageCalBase.build_dow_grid()

    def __init__(self, year: int):
        """
        Creates an instance of OnePageCal for a given year.  The OnePageCalFactory class should be used to create
        an instance of this class for a given year.

        :param year: the year to be used in creating the instance
        :type year: int

        """
        self.year: int = year
        self.first_dow = Day(date(year=year, month=1, day=1).weekday()+1)
        self.month_grid = np.array([[Month.NoMonth for _ in range(0, 7)] for _ in range(0, 4)])
        self.max_dom = max_dom
        if calendar.isleap(year):
            self.max_dom[Month.February] = 29

    def set_month(self, dow: Day, month: Month):
        """
        This method places a Month value in the appropriate cell of the Month grid.  The column index is derived
        from the Day value that corresponds to the Months first day and the row index is the first row within
        the column that has not had a Month assigned to it.

        :param dow: The day of the week of the first day of the specified month
        :type dow: one_page_calendar.model.Day
        :param month: The month to be placed in the Month grid
        :type month: one_page_calendar.model.Month
        :return: None
        """
        idx: int = 0
        while self.month_grid[idx, dow.value-1] != Month.NoMonth:
            idx += 1
        self.month_grid[idx, dow.value-1] = month

    def mo_col_idx(self, month: Month) -> int:
        """
        This method returns the column index to which the specified Month was assigned by the set_month method.

        :param month: The month whose column index will be returned
        :type month: one_page_calendar.model.Month
        :return: the column index
        :rtype: int

        """
        return np.argwhere(self.month_grid == month)[0][1]

    def dow_for_dom(self, month: Month, dom: int) -> Day:
        """
        This method returns the Day the corresponds to the specified Month and day of month

        :param month: The specified Month
        :type month: one_page_calendar.model.Month
        :param dom: the specified day of the month
        :type dom: int
        :return: the day of the week that corresponds to the specified Month and Day of Month
        :rtype: one_page_calendar.model.Day

        """
        dom_row_idx = np.argwhere(OnePageCal.dom_grid == dom)[0][0]
        return OnePageCal.dow_grid[dom_row_idx, self.mo_col_idx(month)]

    def doms_for_dow(self, month: Month, dow: Day) -> list[int]:
        """
        This method returns the days of the month within the specified Month that the specified Day of the Week falls

        :param month: The specified Month
        :type month: one_page_calendar.model.Month
        :param dow: The specified Day of the week
        :type dow: one_page_calendar.model.Day
        :return: a list containing the days of the month as described above
        :rtype: list[int]

        """
        dow_row_idx = np.argwhere(self.dow_grid[0:7, self.mo_col_idx(month)] == dow)[0][0]
        doms = [dom for dom in OnePageCal.dom_grid[dow_row_idx: dow_row_idx+1, 0:7][0] if dom <= self.max_dom[month]]
        return doms


    @staticmethod
    def dom_rows():
        """
        This method returns the rows of the Day of the Month grid

        :returns: yields the rows of the Day of the Month grid one row at a time
        :rtype: np.array

        """
        for row_idx in range(0, 7):
            yield OnePageCal.dom_grid[row_idx: row_idx+1, 0:5][0]

    @staticmethod
    def dow_rows():
        """
        This method returns the rows of the Days of the Week grid

        :return: yields the rows of the Days of the Week grid one row at a time
        :rtype: np.array

        """
        for row_idx in range(0, 7):
            yield OnePageCal.dow_grid[row_idx: row_idx+1, 0:7][0]

    def month_rows(self):
        """
        This method returns the rows of the Month grid

        :return: yields the rows of the Month gris one row at a time
        :rtype: np.array

        """
        for row_idx in range(0, 4):
            yield self.month_grid[row_idx: row_idx+1, 0:7][0]


class OnePageCalFactory:
    """
    A factory class used to create a OnePageCal instance for a given year

    """

    @staticmethod
    def for_year(year: int) -> OnePageCal:
        """
        This method should be used to create instances of OnePageCal rather than invoking the class' __init__ method
        directly.

        :param year: the year to be used in creating the OnePageCal instance
        :type year: int
        :return: a OnePageCal instance for the specified year
        :rtype: one_page_calendar.model.OnePageCal

        """
        cal = OnePageCal(year)
        for month in Month:
            if month != Month.NoMonth:
                first_dow = Day(date(year=year, month=month.value, day=1).weekday()+1)
                cal.set_month(first_dow, month)
        return cal


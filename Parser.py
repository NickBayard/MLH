import re
import bs4
from datetime import datetime
from copy import copy


class ParseError(Exception):
    pass


class ParseChildIdError(ParseError):
    pass


class ParseAvailableDatesError(ParseError):
    pass


class Parser:
    """Parser is essentially the web page scraper that returns various
    bits of information on a particular page."""

    @staticmethod
    def get_child_ids(text):
        soup = bs4.BeautifulSoup(text, 'lxml')

        ids = [i['name'] for i in soup.find_all('input', {'type': 'checkbox'})]

        names = [font.text.strip() for font in soup.find_all('font')
                 if len(font.text.strip()) > 2][-1].split()

        if len(names) != len(ids):
            raise ParseChildIdError

        for index, name in enumerate(copy(names)):
            names[index] = name[:-2] if name.endswith('18') else name

        child_ids = dict(zip(names, ids))

        return child_ids

    @staticmethod
    def get_available_dates(text):
        soup = bs4.BeautifulSoup(text, 'lxml')

        dates = soup.find_all('td', {'class': 'calendar-available'})
        links = [date.find('a')['href'] for date in dates]

        open_dates = []
        for link in links:
            m = re.search("dosubmit\('(\d{8})',", link)
            if m:
                open_dates.append(datetime.strptime(m.group(1), '%Y%m%d').date())

        if not open_dates:
            raise ParseAvailableDatesError

        return open_dates

    @staticmethod
    def get_available_times(text):
        soup = bs4.BeautifulSoup(text, 'lxml')

        times = soup.find_all('form', {'name': 'gridSubmitForm'})

        formatted_times = [time.find('input', {'name': 'appt_start_time'})['value'] for time in times]

        return formatted_times

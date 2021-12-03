import requests
import logging
from datetime import date
import re

logger = logging.getLogger("Results.scraping")


def getpage(url, name):
    r = requests.get(url)
    if r.status_code > 299:
        logger.warning(f"No results available for {name}")
        return ""
    html = r.text
    return html


def find_from_date(weeks, mydate):
    assert weeks >= 0
    assert isinstance(mydate, date)
    from_year = mydate.year
    current_week = mydate.isocalendar()[1]
    from_week = current_week - weeks
    remaining_weeks = weeks - current_week
    while remaining_weeks >= 0:
        from_year -= 1
        weeks_in_from_year = date.fromisoformat(f'{from_year}-12-28').isocalendar()[1]
        from_week = weeks_in_from_year - remaining_weeks
        remaining_weeks -= weeks_in_from_year
    from_date = date.fromisocalendar(from_year, from_week, 1)
    return from_date


def lookup_month_index_from_abbr(month_abbr):
    try:
        month_index = 1 + ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
         'jul', 'aug', 'sep', 'oct', 'nov', 'dec'].index(month_abbr[:3].lower())
    except Exception:
        month_index = 1
    return month_index

def seconds_from_timestring(timestring):
    regexp = re.compile("[.,:;' dhms]")
    stripped = regexp.sub(" ", timestring).strip()
    split = re.split(" ", stripped)
    secs = 0
    n = len(split)-1
    for idx, val in enumerate(split):
        try:
            secs += int(val)*pow(60,n-idx)
        except:
            secs = 0
            break
    if secs > 0 and(len(split) == 4):
        secs = secs - int(split[0])*pow(60,3) + int(split[0])*24*3600
    return secs
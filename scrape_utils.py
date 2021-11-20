import requests
import logging


logger = logging.getLogger("Results.scraping")


def getpage(url, name):
    r = requests.get(url)
    if r.status_code > 299:
        logger.warning(f"No results available for {name}")
        return ""
    html = r.text
    return html


def find_from_date(weeks):
    today = date.today()
    from_year = today.year
    current_week = today.isocalendar().week
    if current_week > weeks:
        from_week = current_week - weeks
    else:
        from_year -= 1
        weeks_in_from_year = date.fromisoformat(f'{from_year}-12-31').isocalendar().week
        from_week = weeks_in_from_year - (weeks - current_week)
    from_date = date.fromisocalendar(from_year, from_week, 0)
    return from_date


def lookup_month_index_from_abbr(month_abbr):
    try:
        month_index = 1 + ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(month_abbr)
    except Exception:
        month_index = 1
    return month_index
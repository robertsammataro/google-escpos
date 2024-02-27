import json
from datetime import *
from escpos import *
from gcal import *

global prefs


def load_user_prefs(filepath='pref.json') -> dict:
    """
        Loads the user's preferences
        Args:
            filepath: str - Filepath to the user's preferences file. Defaults ot pref.json in
                            the CWD but can also be manually supplied.
    """
    with open(filepath) as f:
        data = json.load(f)
    return data


def test_printer(p: printer) -> None:
    """
        Tests the connection of the printer by sending a print command to the
        specified ESC/POS Device
    """
    p.ln(40)
    p.text("Hello World! If you're reading this I'm configured correctly! :D")
    p.ln(40)


def generate_report(p: printer, calendar_id: str = 'primary') -> None:
    """
        Generates a report of all scheduled events for the day and sends the report
        to the printer.
        Args:
            p: printer       - escpos.printer the date will be printed to
            calendar_id: str - calendar_id of the calendar that will be printed.
    """

    p.set(double_height=True, double_width=True)
    p.set(height=3, width=3, custom_size=True)
    p.line_spacing(3)
    p.text('Good Morning, ' + prefs['name'] + '!\n')
    p.set(height=2, width=2, custom_size=True)
    p.text("Today is ")
    p_date(p, multiline=False)
    p.ln(10)
    p.textln('Here\'s a look at your day:')
    p.ln(25)
    p_calendar(p, calendar_id)


prefs = load_user_prefs()

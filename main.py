import os
import json
from datetime import *
from escpos import *
from apiCaller import *

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
    

def p_date(p: printer, weekday=True, multiline=False) -> None:
    """
        Prints the current date on the specified ESC/POS Device
        Args:
            p: printer    - escpos.printer the date will be printed to
            weekday: bool - Determines whether the day of the week will be
                            printed (True=Yes, False=No)
    """
    
    dt = datetime.now()
    if weekday:
        p.text(dt.strftime('%A, '))
    if multiline:
        p.text(dt.strftime('\n'))
    p.textln(dt.strftime('%d %B %Y'))

def p_calendar(p: printer, calendar_id) -> None:
    """
        Prints the specified calendar with formatting. Includes event name,
        time, and location (if applicable)
        Args:
            p: printer       - escpos.printer the date will be printed to
            calendar_id: str - calendar_id of the calendar that will be printed.
    """
    for item in retrieve_events(calendar_id=calendar_id, sort=True):
        p.set(height=3, width=3, custom_size=True)
        p.textln(item['summary'])
        p.set(height=2, width=2, custom_size=True)
        p.textln(to_local_tz(parse_result_to_time(item['start']['dateTime'])).strftime("%I:%M %p") + " - " + to_local_tz(parse_result_to_time(item['end']['dateTime'])).strftime("%I:%M %p"))
        p.ln(5)
        try:
          p.text(item['location'])
          p.ln(2)
        except:
          continue
    
    p.ln(100)

def generate_report(p: printer, calendar_id: str='primary') -> None:
    """
        Generates a report of all scheduled events for the day and sends the report
        to the printer.
        Args:
            p: printer       - escpos.printer the date will be printed to
            calendar_id: str - calendar_id of the calendar that will be printed.
    """
    
    p = printer.Serial("COM4")
    p.set(double_height=True, double_width=True, height=3, width=3, custom_size=True)
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
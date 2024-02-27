import os
from datetime import *
from escpos import *
from apiCaller import *

# Prompts the user to enter their information which will be saved later.
def onboard_user() -> None:
    return

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

def generate_report() -> None:
    #pp.pprint(retrieve_events())
    p = printer.Serial("COM4")
    p.set(double_height=True, double_width=True)
    p.set(height=3, width=3, custom_size=True)
    p.line_spacing(3)
    p.text('Good Morning, Robby!\n')
    p.set(height=2, width=2, custom_size=True)
    p.text("Today is ")
    p_date(p, multiline=False)
    p.ln(10)
    p.textln('Here\'s a look at your day:')
    p.ln(25)
    
    for item in retrieve_events(calendar_id='rsammataro1126@gmail.com', sort=True):
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
    

if __name__ == "__main__":
    generate_report()
import datetime
import os.path
import pprint
from datetime import datetime, timedelta
from tzlocal import get_localzone
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
pp = pprint.PrettyPrinter(indent=4)

# Parse the date string returned from Google into a Python datetime object
def parse_result_to_datetime(d_string: str) -> datetime:
    """
      When called takes the input string and converts it to a timezone-aware datetime object.
      Designed to take in the datetime string returned by the Google API and automatically
      convert it.
      
      Google API Timestamp format: Format YYYY-MM-DDTHH:MM:SS+DH:DM
      
      Args:
          d_string: str - This is the datetime string associated with an event on the Google Calendar.
    """
    dt = datetime.strptime(d_string, '%Y-%m-%dT%H:%M:%S%z')
    return dt

def parse_result_to_time(d_string: str) -> datetime:
    """
      NOTE: This function should generally not be used. It only serves to fix a problem where repeating events
      in Google Calendar return with a start date of its first occurance. parse_result_to_datetime() should
      generally be used instead. USING THIS FUNCTION RETURNS A DATETIME OBJECT WITH A DATE OF 1900-01-01

      When called takes the input string and converts it to a timezone-aware datetime object WITH NO ATTACHED DATE.
      Designed to take in the datetime string returned by the Google API and automatically convert it.
      
      Args:
          d_string: str - This is the datetime string associated with an event on the Google Calendar.
    """
    d_string = d_string.split('T')
    dt = datetime.strptime(d_string[1], '%H:%M:%S%z')
    return dt
    

def to_local_tz(dt: datetime) -> datetime:
    """
      Converts datetime object to the computer's local timezone
      
      Args:
          dt: datetime - Timezone aware datetime object being localized.
    """
    return dt.astimezone(get_localzone())
    
def insert_event(sorted_events: dict, new_event: dict) -> dict:
    """
      Inserts event dictionaries into a list such that the earliest occuring events are in the front
      of the list and the latest occuring events are in the back. 
      
      Args:
          sorted_events: dict[] - Sorted list of Google Calendar events that the event will be inserted into
          new_event: dict       - New event dictionary that will be inserted into sorted_events
    """
    
    count = 0   
    while count < len(sorted_events):
        if(parse_result_to_time(new_event['start']['dateTime']) < parse_result_to_time(sorted_events[count]['start']['dateTime'])):
            sorted_events.insert(count, new_event)
            return sorted_events
        count += 1
    
    sorted_events.append(new_event)
    return sorted_events



def retrieve_events(calendar_id='primary', day=None, sort=True):
  """
    When called prompts the user to log into their Google Account (if a valid token file does
    not already exist) and queries all events from the specified calendar on the specified day.
    
    Args:
        calendar_id: string - This is the calendar_id of the calendar that will be queried.
        day: string         - This is a user-specified day that events will be queried for.
                              String must be in YYYY-MM-DD format (Ex: 2024-03-05).
        sort: bool          - Defines whether or not to sort the found events by start time before returning
                              (sort=True) or in the order returned from the API call (sort=False)
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)
        
    calendar = service.calendars().get(calendarId=calendar_id).execute()
    
    ##Retrieves all the data from the specified calendar within the time range.
    page_token = None
    found_events = []
    
    while True:
        
        now = datetime.now()
        
        starttime = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=get_localzone())
        endtime = datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=get_localzone())
        
        # Target events on a user provided date
        if day:
            
            c_date = day.split('-')
            c_year = int(c_date[0])
            c_month = int(c_date[1])
            c_day = int(c_date[2])
            
            starttime = datetime(c_year, c_month, c_day, 0, 0, 0, tzinfo=get_localzone())
            endtime = datetime(c_year, c_month, c_day, 23, 59, 59, tzinfo=get_localzone())
        
        t_start = starttime.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        t_end = endtime.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        events = service.events().list(calendarId=calendar_id, timeMin=t_start, timeMax=t_end, pageToken=page_token).execute()
        for event in events['items']:
            if sort:
                found_events = insert_event(found_events, event)
            else:
                found_events.append(event)
            
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    return found_events

  except HttpError as error:
    print(f"An error occurred: {error}")    
    return None


"""
        TODO: Come back and make this an available function!!!!!

    """
    # This segment retrieves all of the calendars associated with the current user's Google account
    #page_token = None
    #while True:
    #    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    #    for calendar_list_entry in calendar_list['items']:
    #        print(calendar_list_entry)
    #    page_token = calendar_list.get('nextPageToken')
    #    if not page_token:
    #        break
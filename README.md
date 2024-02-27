# google-escpos
A Python project to connect ESCPOS capable Thermal Printers to generate reports through the use of the Google API. 

## Hey there 👋
Have you ever wanted to start your morning off with a report of your day's activities already written down on paper? Are you the kind of person that wants to easily print your to-do lists and shopping lists onto a physical piece of paper? Well you can do that and even more with google-escpos: a python project that aims to make it easy to print from services like Google Calendar or Google Keep directly onto a connected thermal printer.

> [!IMPORTANT]  
> You will need to get your own API keys for accessing Google's services with this repository. For a walkthrough of how to do this, follow these instructions. (Coming Soon)

## Prerequisites
Running the google-escpos project requires a few python libraries, all of which can be installed via pip. The required libraries for google-escpos are:
- pytz (Python Timezone Library)
- tzlocal (Local Timezone Library)
- google-api-python-client (For using the Google API)

## Developer Plans
The google-escpos project is still in its infancy, and there are still plenty of features that are planned to be added. Some of the features in the works are:
- Support for printing Google Calendar events
- Printing events from multiple Google Calendars
- Printing Google Keep notes

This list isn't inclusive, though, and more features will be added in the future. These are just the big ones for now that work will be focused around.

> [!NOTE]  
> This repository has been built and tested using a Canon RP10 Receipt Printer. It's possible (and very likely) there will be issues when using other thermal printers. Forks/Pull Requests are welcome and encouraged to help expand compatibility with other ESC/POS capable devices.

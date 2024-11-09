import requests
from datetime import datetime, timedelta, timezone
import config


# Mailgun API details
API_KEY = config.MAILGUN_API_KEY
DOMAIN_NAME = config.MAILGUN_DOMAIN
BASE_URL = f'https://api.mailgun.net/v3/{DOMAIN_NAME}/events'

# Auth for API
auth = ('api', API_KEY)

# Function to convert events to CSV format
def events_to_csv(events):
    csv_data = "Event,Timestamp,Recipient , Sender\n"
    for event in events:
        event_data = event.get('event', 'Unknown Event')
        timestamp = datetime.utcfromtimestamp(event.get('timestamp', ''))
        event['timestamp'] = timestamp
        recipient = event.get('recipient', 'Unknown Recipient')
        sender = event['message']['headers']['from']
        csv_data += f"{event_data},{timestamp},{recipient},{sender}\n"
    return csv_data

# Function to fetch email events from Mailgun
def fetch_email_events():
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=2)

    # Format times for API request (Mailgun uses RFC-2822 or epoch time)
    start_time_str = start_time.strftime('%a, %d %b %Y %H:%M:%S +0000')
    end_time_str = end_time.strftime('%a, %d %b %Y %H:%M:%S +0000')

    # Parameters for filtering events
    params = {
        'begin': start_time_str,
        'end': end_time_str,
        'limit': 100  # Limit number of events (can adjust as needed)
    }

    # Make the GET request to Mailgun API
    response = requests.get(BASE_URL, auth=auth, params=params)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        events = data.get('items', [])
        return events
    else:
        return []

event = fetch_email_events()
csv = events_to_csv(event)
print(csv)
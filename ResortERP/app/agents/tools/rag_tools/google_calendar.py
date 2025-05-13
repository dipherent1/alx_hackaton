# app/agents/calendar_tools.py
# Inside app/agents/tools/rag_tools/google_calendar.py (or calendar_tools.py)

import datetime
import os.path # Make sure os is imported
from typing import List, Dict, Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- Define scopes ---
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# --- Calculate paths relative to THIS file ---
TOKEN_PATH = "app/agents/tools/rag_tools/token.json"
CREDS_PATH = "app/agents/tools/rag_tools/credentials.json"
# Add a print statement for debugging (optional, remove later)
print(f"[Calendar Tools] Using Token Path: {TOKEN_PATH}")
print(f"[Calendar Tools] Using Creds Path: {CREDS_PATH}")


if not os.path.exists(TOKEN_PATH):
    print(f"ERROR: Token path does not exist: {TOKEN_PATH}")
if not os.path.exists(CREDS_PATH):
    print(f"ERROR: Credentials path does not exist: {CREDS_PATH}")

def _get_calendar_credentials() -> Optional[Credentials]:
    """
    Handles non-interactive loading and refreshing of Google credentials.
    Relies on existing token.json and credentials.json using absolute paths.

    Returns:
        Credentials object if successful, None otherwise.
    """
    creds = None
    # Use the absolute TOKEN_PATH
    print(f"DEBUG: Checking for token file at: {TOKEN_PATH}") # More debugging
    if os.path.exists(TOKEN_PATH):
        print(f"DEBUG: Token file FOUND at: {TOKEN_PATH}")
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except ValueError as ve:
             print(f"Error loading credentials from token file '{TOKEN_PATH}'. Is it valid JSON? Error: {ve}")
             return None
        except Exception as e:
            print(f"Error loading credentials from {TOKEN_PATH}: {e}")
            return None # Indicate failure to load
    else:
        print(f"DEBUG: Token file NOT FOUND at: {TOKEN_PATH}")


    # If there are no valid credentials available, try to refresh.
    if not creds or not creds.valid:
        print("DEBUG: Credentials not found or not valid. Checking refresh token...")
        # Use the absolute CREDS_PATH for refresh context
        print(f"DEBUG: Expecting credentials file for refresh at: {CREDS_PATH}")
        if creds and creds.expired and creds.refresh_token:
            print(f"DEBUG: Credentials expired, attempting refresh using {CREDS_PATH}...")
            if not os.path.exists(CREDS_PATH):
                 print(f"ERROR: Cannot refresh token. Credentials file missing at {CREDS_PATH}")
                 return None
            try:
                creds.refresh(Request())
                # Save the refreshed credentials to the absolute TOKEN_PATH
                with open(TOKEN_PATH, "w") as token:
                    token.write(creds.to_json())
                print("DEBUG: Credentials refreshed successfully.")
            except Exception as e:
                print(f"Failed to refresh credentials: {e}")
                # Consider deleting token.json here if refresh fails permanently
                # if os.path.exists(TOKEN_PATH): os.remove(TOKEN_PATH)
                return None # Indicate failure
        else:
            # Cannot proceed without a valid token.json or refresh token
            print(f"ERROR: Cannot authenticate Google Calendar.")
            if not os.path.exists(TOKEN_PATH):
                 print(f"Reason: Token file missing at '{TOKEN_PATH}'.")
            elif not creds:
                 print(f"Reason: Failed to load credentials from '{TOKEN_PATH}'.")
            elif not creds.valid:
                 print(f"Reason: Credentials loaded from '{TOKEN_PATH}' are invalid.")
            if not (creds and creds.refresh_token):
                print("Reason: No valid refresh token found to attempt refresh.")

            print(f"Please ensure '{TOKEN_PATH}' exists and is valid (run interactive auth if needed).")
            print(f"Ensure '{CREDS_PATH}' is also present for potential refresh.")
            return None # Indicate failure - requires pre-authentication

    print("DEBUG: Credentials obtained successfully.")
    return creds

# ... (rest of your calendar tool functions: _build_calendar_service,
#      _format_event, tool_get_next_10_calendar_events,
#      tool_get_calendar_events_in_range) ...
# --- Make sure they all use the _get_calendar_credentials() function ---

def _build_calendar_service(creds: Credentials) -> Optional[Any]:
    """Builds the Google Calendar API service client."""
    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except Exception as e:
        print(f"Error building Google Calendar service: {e}")
        return None

def _format_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Helper to format an event dictionary for consistent return."""
    start = event.get("start", {}).get("dateTime", event.get("start", {}).get("date"))
    # Ensure start is a string (convert date objects if necessary)
    if isinstance(start, (datetime.date, datetime.datetime)):
        start = start.isoformat()
    return {
        "summary": event.get("summary", "No Title"),
        "start": start,
        "id": event.get("id")
        # Add other fields if needed, e.g., end, description
    }

# --- Agent Tool: Get Next 10 Events ---
def tool_get_next_10_calendar_events() -> Dict[str, Any]:
    """
    Retrieves the next 10 upcoming events from the user's primary Google Calendar.

    Returns:
        dict: A dictionary containing either a 'events' key with a list of
              event details (summary, start time/date, id) or an 'error' key
              with an error message.
    """
    print("Attempting to get next 10 calendar events...")
    creds = _get_calendar_credentials()
    if not creds:
        return {"error": "Authentication failed. Cannot access Google Calendar."}

    service = _build_calendar_service(creds)
    if not service:
        return {"error": "Failed to build Google Calendar service."}

    try:
        # Use timezone-aware UTC now for timeMin
        now_utc = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now_utc,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        items = events_result.get("items", [])

        if not items:
            return {"events": [], "message": "No upcoming events found."} # Return empty list

        formatted_events = [_format_event(event) for event in items]
        print(f"Successfully retrieved {len(formatted_events)} upcoming events.")
        return {"events": formatted_events}

    except HttpError as error:
        print(f"An HTTP error occurred getting events: {error}")
        return {"error": f"Google Calendar API error: {error.resp.status} - {error.reason}"}
    except Exception as e:
        print(f"An unexpected error occurred getting events: {e}")
        return {"error": f"An unexpected error occurred: {str(e)}"}


# --- Agent Tool: Get Events in Date Range ---
def tool_get_calendar_events_in_range(start_time_str: str, end_time_str: str) -> Dict[str, Any]:
    """
    Retrieves events from the user's primary Google Calendar within a specific date/time range.

    Args:
        start_time_str (str): The start date/time in ISO 8601 format (e.g., '2023-10-27T10:00:00Z' or '2023-10-27').
                              The agent should provide this format.
        end_time_str (str): The end date/time in ISO 8601 format (e.g., '2023-10-28T17:00:00Z' or '2023-10-28').
                            The agent should provide this format.

    Returns:
        dict: A dictionary containing either an 'events' key with a list of
              event details (summary, start time/date, id) found in the range
              or an 'error' key with an error message.
    """
    print(f"Attempting to get calendar events from {start_time_str} to {end_time_str}...")
    creds = _get_calendar_credentials()
    if not creds:
        return {"error": "Authentication failed. Cannot access Google Calendar."}

    service = _build_calendar_service(creds)
    if not service:
        return {"error": "Failed to build Google Calendar service."}

    # Validate and parse date strings - agent needs to provide correct format
    try:
        # Use fromisoformat which handles dates and datetimes with/without timezone
        start_dt = datetime.datetime.fromisoformat(start_time_str)
        end_dt = datetime.datetime.fromisoformat(end_time_str)

        # Convert to ISO format strings suitable for the API (ensure timezone if needed)
        # The API generally expects RFC3339, which isoformat provides.
        # Add UTC timezone if none is present for consistency? Or let API handle local time?
        # Let's assume the input string dictates the intended timezone or lack thereof.
        start_iso = start_dt.isoformat()
        end_iso = end_dt.isoformat()

    except ValueError:
        return {"error": "Invalid date/time format. Please use ISO 8601 format (e.g., 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SSZ')."}
    except Exception as e:
         return {"error": f"Error processing date/time strings: {str(e)}"}


    try:
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_iso,
                timeMax=end_iso,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        items = events_result.get("items", [])

        if not items:
            return {"events": [], "message": "No events found in the specified range."} # Return empty list

        formatted_events = [_format_event(event) for event in items]
        print(f"Successfully retrieved {len(formatted_events)} events in range.")
        return {"events": formatted_events}

    except HttpError as error:
        print(f"An HTTP error occurred getting events in range: {error}")
        return {"error": f"Google Calendar API error: {error.resp.status} - {error.reason}"}
    except Exception as e:
        print(f"An unexpected error occurred getting events in range: {e}")
        return {"error": f"An unexpected error occurred: {str(e)}"}
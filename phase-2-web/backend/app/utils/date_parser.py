"""Natural language date parsing utilities"""
from datetime import datetime, timedelta
from typing import Optional
from dateutil import parser
from dateutil.relativedelta import relativedelta
import re


def parse_natural_date(date_string: str) -> Optional[datetime]:
    """
    Parse natural language date strings into datetime objects.

    Supports formats like:
    - "tomorrow", "today", "yesterday"
    - "next monday", "next week", "next month"
    - "in 3 days", "in 2 weeks", "in 1 month"
    - Standard date formats: "2026-02-10", "Feb 10, 2026"

    Args:
        date_string: Natural language date string

    Returns:
        datetime object or None if parsing fails
    """
    if not date_string:
        return None

    date_string = date_string.lower().strip()
    now = datetime.now()

    # Handle relative dates
    if date_string == "today":
        return now.replace(hour=23, minute=59, second=59)

    if date_string == "tomorrow":
        return (now + timedelta(days=1)).replace(hour=23, minute=59, second=59)

    if date_string == "yesterday":
        return (now - timedelta(days=1)).replace(hour=23, minute=59, second=59)

    # Handle "next [day of week]"
    weekdays = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6
    }

    for day_name, day_num in weekdays.items():
        if f"next {day_name}" in date_string or date_string == day_name:
            days_ahead = day_num - now.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return (now + timedelta(days=days_ahead)).replace(hour=23, minute=59, second=59)

    # Handle "in X days/weeks/months"
    in_pattern = r"in (\d+) (day|days|week|weeks|month|months)"
    match = re.search(in_pattern, date_string)
    if match:
        amount = int(match.group(1))
        unit = match.group(2)

        if "day" in unit:
            return (now + timedelta(days=amount)).replace(hour=23, minute=59, second=59)
        elif "week" in unit:
            return (now + timedelta(weeks=amount)).replace(hour=23, minute=59, second=59)
        elif "month" in unit:
            return (now + relativedelta(months=amount)).replace(hour=23, minute=59, second=59)

    # Handle "next week/month"
    if "next week" in date_string:
        return (now + timedelta(weeks=1)).replace(hour=23, minute=59, second=59)

    if "next month" in date_string:
        return (now + relativedelta(months=1)).replace(hour=23, minute=59, second=59)

    # Try standard date parsing
    try:
        parsed_date = parser.parse(date_string, fuzzy=True)
        # If no time specified, set to end of day
        if parsed_date.hour == 0 and parsed_date.minute == 0:
            parsed_date = parsed_date.replace(hour=23, minute=59, second=59)
        return parsed_date
    except (ValueError, parser.ParserError):
        return None


def parse_recurrence_pattern(recurrence_string: str) -> Optional[dict]:
    """
    Parse natural language recurrence patterns.

    Supports formats like:
    - "daily", "every day"
    - "weekly", "every week", "every monday"
    - "monthly", "every month"
    - "every 2 days", "every 3 weeks"

    Args:
        recurrence_string: Natural language recurrence string

    Returns:
        Dictionary with recurrence pattern or None if parsing fails
    """
    if not recurrence_string:
        return None

    recurrence_string = recurrence_string.lower().strip()

    # Daily patterns
    if "daily" in recurrence_string or "every day" in recurrence_string:
        return {"type": "daily", "interval": 1}

    # Weekly patterns
    if "weekly" in recurrence_string or "every week" in recurrence_string:
        return {"type": "weekly", "interval": 1}

    # Monthly patterns
    if "monthly" in recurrence_string or "every month" in recurrence_string:
        return {"type": "monthly", "interval": 1}

    # Specific day of week
    weekdays = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6
    }

    for day_name, day_num in weekdays.items():
        if f"every {day_name}" in recurrence_string:
            return {"type": "weekly", "interval": 1, "days_of_week": [day_num]}

    # Pattern with interval: "every X days/weeks/months"
    interval_pattern = r"every (\d+) (day|days|week|weeks|month|months)"
    match = re.search(interval_pattern, recurrence_string)
    if match:
        interval = int(match.group(1))
        unit = match.group(2)

        if "day" in unit:
            return {"type": "daily", "interval": interval}
        elif "week" in unit:
            return {"type": "weekly", "interval": interval}
        elif "month" in unit:
            return {"type": "monthly", "interval": interval}

    return None

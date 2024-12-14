from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from calendar import monthcalendar, month_name
from datetime import datetime
from typing import Optional, Tuple

class CalendarKeyboard:
    @staticmethod
    def create_calendar(year: int, month: int) -> InlineKeyboardMarkup:
        """
        Creates calendar keyboard with month/year header, weekday headers, 
        day buttons, and navigation.

        Args:
            year (int): Year to display
            month (int): Month to display (1-12)

        Returns:
            InlineKeyboardMarkup: Calendar keyboard markup
        """
        keyboard = [
            # Header row with month and year
            [InlineKeyboardButton(text=f"{month_name[month]} {year}", callback_data="ignore")],
            
            # Weekday headers
            [InlineKeyboardButton(text=day, callback_data="ignore") 
             for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]],
        ]
        
        # Add day buttons
        for week in monthcalendar(year, month):
            row = []
            for day in week:
                if day == 0:
                    # Empty day
                    row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
                else:
                    # Valid day
                    callback_data = f"calendar:select:{year}:{month}:{day}"
                    row.append(InlineKeyboardButton(text=str(day), callback_data=callback_data))
            keyboard.append(row)
            
        # Navigation buttons
        keyboard.append([
            InlineKeyboardButton(text="◀️", callback_data=f"calendar:prev:{year}:{month}"),
            InlineKeyboardButton(text="❌", callback_data="calendar:cancel"),
            InlineKeyboardButton(text="▶️", callback_data=f"calendar:next:{year}:{month}")
        ])
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @staticmethod
    def process_selection(callback_data: str) -> Optional[Tuple[int, int, int]]:
        """
        Process calendar callback data and return selected date or None.

        Args:
            callback_data (str): Callback data from calendar button

        Returns:
            Optional[Tuple[int, int, int]]: (year, month, day) if date selected, None otherwise
        """
        parts = callback_data.split(":")
        if len(parts) != 5 or parts[0] != "calendar":
            return None
            
        action = parts[1]
        if action != "select":
            return None
            
        try:
            year = int(parts[2])
            month = int(parts[3])
            day = int(parts[4])
            return year, month, day
        except (ValueError, IndexError):
            return None

    @staticmethod
    def get_next_month(year: int, month: int) -> Tuple[int, int]:
        """Get next month and year."""
        if month == 12:
            return year + 1, 1
        return year, month + 1

    @staticmethod
    def get_prev_month(year: int, month: int) -> Tuple[int, int]:
        """Get previous month and year."""
        if month == 1:
            return year - 1, 12
        return year, month - 1

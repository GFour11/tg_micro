"""Bot command messages and responses."""

# Main menu command descriptions
COMMANDS_DESCRIPTION = {
    "start": "Show main menu",
    "about": "About section",
    "dashboard": "Dashboard",
    "bots": "Bots management",
    "settings": "Settings"
}

# Command responses
MAIN_MENU_TEXT = """
🤖 <b>Main Menu</b>

Available commands:
/start - Show this menu
/about - About section
/dashboard - Dashboard
/bots - Bots management
/settings - Settings
"""

ABOUT_TEXT = """
📝 <b>About</b>

This is a Telegram bot built with aiogram 3.14.0.
It provides various management features through a command-based interface.
"""

DASHBOARD_TEXT = """
📊 <b>Dashboard</b>

Your dashboard information will be displayed here.
"""

BOTS_TEXT = """
🤖 <b>Bots Management</b>

Here you can manage your bots.
"""

SETTINGS_TEXT = """
⚙️ <b>Settings</b>

Configure your bot settings here.
"""

# Navigation responses
BACK_BTN_TEXT = "⬅️ Back"

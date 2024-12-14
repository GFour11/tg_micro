# Main menu messages
YOUR_BOTS = "Your Bots:"
NO_BOTS = "You don't have any active bots yet."

# Bot types
BOT_TYPES = {
    "BACKTEST": "Backtesting",
    "VIRTUAL": "Virtual Bot (paper trading)",
    "REAL": "Real Bot"
}

# Creation flow messages
SELECT_BOT_TYPE = "Select the type of bot you want to create:"
SELECT_SIGNAL_OR_CLASSIC = "Select signal or classic Bot."
SELECT_START_DATE = "Select the start date for backtesting:"
SELECT_END_DATE = "Select the end date for backtesting:"
SELECT_SIGNAL = "Choose the signal type for your bot:"
HOW_TO_SETUP_ALERT = "How to set up alerts:/n<code>[Instructions Placeholder]</code>"
ENTER_BOT_NAME = "Add unique name for bot:"
SETUP_EXCHAGE_OR_QUOTE = "Do you want to set up exchange before choose quota?"
ENTER_QUOTE = "Enter the qoute:"
ENTER_MAX_TOTAL_BALANCE = "Enter the maximum total balance for trading:"
MAX_ACTIVE_BOTS_PER_SYMBOL = "Enter the maximum number of active bots per symbol:"
ENTER_EXCHANGE = "Enter the exchange name:"
ENTER_SYMBOL = "Enter the trading symbol (e.g., BTC/USDT):"
ENTER_MAX_BALANCE = "Enter the maximum balance for trading:"
ENTER_PROFIT_TARGET = "Enter your profit target percentage:"
ENTER_MAX_RISK = "Enter the maximum risk percentage:"
ENTER_PRICE_LIMIT = "Enter the price limit for trades:"
SELECT_STRATEGY = "Do you want to set up advanced strategy parameters or launch now?"
SELECT_API_KEY = "Select the API key:"

# Signal types
SIGNAL_TYPES = {
    "TRADINGVIEW": "TradingView",
    "VOLUME": "Volume Spikes",
    "RETRACEMENT": "Retracement",
    "BOUNCE": "Daily Bounce"
}

# Bot management messages
BOT_STOPPED = "Bot has been stopped successfully."
BOT_STARTED = "Bot has been started successfully."

# Validation messages
INVALID_DATE = "❌ Invalid date selection. Please try again."
INVALID_RANGE = "❌ End date must be after start date."
FUTURE_DATE = "❌ Cannot select future dates."
INVALID_BALANCE = "❌ Invalid balance amount. Please enter a valid number."
INVALID_PERCENTAGE = "❌ Invalid percentage. Please enter a number between 0 and 100."
INVALID_SYMBOL = "❌ Invalid trading symbol format. Please use format like BTC/USDT."

# Confirmation messages
CONFIRM_SETTINGS = "Please confirm your bot settings:"
BOT_CREATED = "✅ Your bot has been created successfully!"
BOT_LAUNCHED = "✅ Your bot has been launched successfully!"
SETTINGS_UPDATED = "✅ Bot settings have been updated successfully!"

# Advanced setup
ADVANCED_SETUP = "Advanced Setup Options:"
STRATEGY_PARAMS = "Strategy Parameters:"
RISK_MANAGEMENT = "Risk Management Settings:"
NOTIFICATION_SETTINGS = "Notification Settings:"
PORTFOLIO_SETTINGS = "Portfolio Management:"
NEW_PORTFOLIO = "Enter unique name:"

BACK_TO_BOTS = "⬅️ Back to Bots"

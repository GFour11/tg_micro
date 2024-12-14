"""Bot configuration settings and environment variables."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class BotConfig:
    """Bot configuration class."""
    token: str

    @property
    def is_configured(self) -> bool:
        """Check if bot is configured properly."""
        return bool(self.token)

# Initialize bot configuration
bot_config = BotConfig(
    token=os.getenv("BOT_TOKEN", "")
)
cipher_key=os.getenv("ENCRYPTION_KEY", "")

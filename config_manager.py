from aqt import mw

class ConfigManager:
    """Manages loading and saving add-on configuration."""

    def __init__(self, addon_name: str):
        self.addon_name = addon_name
        self.config = self.load_config()

    def load_config(self):
        """Load the current configuration from Anki."""
        return mw.addonManager.getConfig(self.addon_name) or {}

    def save_config(self, new_config):
        """Save new configuration settings."""
        mw.addonManager.writeConfig(self.addon_name, new_config)
        self.config = new_config  # Update current instance

    def get(self, key, default=None):
        """Get a configuration value with a default fallback."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a configuration value and save it."""
        self.config[key] = value
        self.save_config(self.config)

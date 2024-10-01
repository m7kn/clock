import yaml
from settings_definition import get_default_config

def tuple_constructor(loader, node):
    """Custom YAML constructor for handling tuples."""
    return list(loader.construct_sequence(node))

yaml.SafeLoader.add_constructor('tag:yaml.org,2002:python/tuple', tuple_constructor)

class ConfigManager:
    """Manages the configuration for the desktop clock application."""

    def __init__(self, config_file):
        """Initialize the ConfigManager with a config file path."""
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Load the configuration from the file, or use default if file not found."""
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Ensure all necessary keys exist with default values
            default_config = get_default_config()
            for section in default_config:
                if section not in config:
                    config[section] = {}
                for key, value in default_config[section].items():
                    if key not in config[section]:
                        config[section][key] = value
                        
            # Convert tuples to lists
            if 'clock' in config:
                if 'color' in config['clock']:
                    config['clock']['color'] = list(config['clock']['color'])
                if 'background_color' in config['clock']:
                    config['clock']['background_color'] = list(config['clock']['background_color'])
            if 'main_window' in config:
                if 'background_color' in config['main_window']:
                    config['main_window']['background_color'] = list(config['main_window']['background_color'])                      

            return config
        except FileNotFoundError:
            return get_default_config()

    def save_config(self):
        """Save the current configuration to the file."""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f)

    def get_config(self):
        """Get the entire configuration dictionary."""
        return self.config

    def get_setting(self, section, key):
        """Get a specific setting value from the configuration."""
        return self.config[section][key]

    def set_setting(self, section, key, value):
        """Set a specific setting value in the configuration and save it."""
        self.config[section][key] = value
        self.save_config()
        
import yaml
from settings_definition import get_default_config

def tuple_constructor(loader, node):
    return list(loader.construct_sequence(node))

yaml.SafeLoader.add_constructor('tag:yaml.org,2002:python/tuple', tuple_constructor)

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
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
                        
            # Konvertáljuk a tuple-öket listákká
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
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f)

    def get_config(self):
        return self.config

    def get_setting(self, section, key):
        return self.config[section][key]

    def set_setting(self, section, key, value):
        self.config[section][key] = value
        self.save_config()
        
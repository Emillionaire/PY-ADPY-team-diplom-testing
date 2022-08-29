import configparser

# Read settings file
path_to_settings = 'settings.ini'
settings_file = configparser.ConfigParser()
settings_file.read(path_to_settings)

# Database block
database = settings_file.get('Database', 'database')
user = settings_file.get('Database', 'user')
password = settings_file.get('Database', 'password')
port = settings_file.get('Database', 'port')
host = settings_file.get('Database', 'host')
reset_scheme_tables = settings_file.get('Database', 'reset_scheme_tables')

# Tokens block
vk_user_token = settings_file.get('Tokens', 'vk_user_token')
vk_group_token = settings_file.get('Tokens', 'vk_group_token')

# VK_API block
URL = settings_file.get('VK_API', 'URL')
URL_search = settings_file.get('VK_API', 'URL_search')

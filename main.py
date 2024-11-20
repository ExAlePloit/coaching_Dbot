from database import DatabaseManager

# Discord Token
with open('DISCORD_TOKEN', 'r') as f:
    DISCORD_TOKEN = f.read()

db_manager = DatabaseManager()
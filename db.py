import sqlite3

default_admins = [
    (1, '1027596128', 1),
    (2, '1068178978', 1)
]
token = '7476318571:AAGj2iJy6zavdPPLO-sGojkwrqq2rBSpClA'
bot_name = 'MRBLACKEY-D-DoS'
bot_username = '@MRBLACKEY_D_DoS_bot'
owner_username = '@MR_BLACKEY'
channel_username = '@MR_BLACKEY_HACKS'

def initialize_db():
    if not os.path.exists('bot_data.db'):
        pass
    else:
        conn = sqlite3.connect('bot_data.db')
        conn.execute('PRAGMA journal_mode=WAL;')
        cursor = conn.cursor()
        cursor.execute("BEGIN IMMEDIATE")
        # Create table for bot configurations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_configs (
                id INTEGER PRIMARY KEY,
                token TEXT NOT NULL,
                bot_name TEXT NOT NULL,
                bot_username TEXT NOT NULL,
                owner_username TEXT NOT NULL,
                channel_username TEXT
            )
        ''')
        
        # Insert default bot config if not exists
        cursor.execute('''
            INSERT OR IGNORE INTO bot_configs (id,token,bot_name,bot_username,owner_username,channel_username)
            VALUES (?,?,?,?,?,?)
        ''', ('1',token,bot_name,bot_username,owner_username,channel_username,))
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                expiration_date DATETIME,
                bot_id INTEGER,
                FOREIGN KEY (bot_id) REFERENCES bot_configs(id)
            )
        ''')
    
        # Create admins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY,
                admin_id TEXT,
                bot_id INTEGER,
                FOREIGN KEY (bot_id) REFERENCES bot_configs(id)
            )
        ''')
        
        # Insert default admin if not exists
        for id,admin_id, bot_id in default_admins:
            cursor.execute('''
                INSERT OR IGNORE INTO admins (id, admin_id, bot_id)
                VALUES (?, ?, ?)
            ''', (id, admin_id, bot_id))
    
        # Create logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                username TEXT,
                target TEXT,
                port INTEGER,
                time INTEGER,
                command TEXT,
                timestamp TEXT
            )
        ''')
    
        conn.commit()
        conn.close()

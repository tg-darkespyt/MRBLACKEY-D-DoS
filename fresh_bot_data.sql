PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE bot_configs (
            id INTEGER PRIMARY KEY,
            token TEXT NOT NULL,
            bot_name TEXT NOT NULL,
            bot_username TEXT NOT NULL,
            owner_username TEXT NOT NULL,
            channel_username TEXT
        );
INSERT INTO bot_configs VALUES(1,'7476318571:AAGj2iJy6zavdPPLO-sGojkwrqq2rBSpClA','MRBLACKEY-D-DoS','@MRBLACKEY_D_DoS_bot','@MR_BLACKEY','@MR_BLACKEY_HACKS');
CREATE TABLE users (
            user_id TEXT PRIMARY KEY,
            expiration_date DATETIME,
            bot_id INTEGER,
            FOREIGN KEY (bot_id) REFERENCES bot_configs(id)
        );
INSERT INTO users VALUES('1196324460','2024-10-18 06:12:33.609823',1);
CREATE TABLE admins (
            id INTEGER PRIMARY KEY,
            admin_id TEXT,
            bot_id INTEGER,
            FOREIGN KEY (bot_id) REFERENCES bot_configs(id)
        );
INSERT INTO admins VALUES(1,'1027596128',1);
INSERT INTO admins VALUES(2,'1068178978',1);
CREATE TABLE logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            target TEXT,
            port INTEGER,
            time INTEGER,
            command TEXT,
            timestamp TEXT
        );
DELETE FROM sqlite_sequence;
COMMIT;

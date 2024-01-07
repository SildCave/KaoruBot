import sqlite3

DatabasePath = "Database.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')

    def create_table(self, table_name, columns):
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

    def insert(self, table_name, columns, values):
        self.conn.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
        self.conn.commit()

    def select(self, table_name, columns, where):
        return self.conn.execute(f"SELECT {columns} FROM {table_name} WHERE {where}")
    
    def update(self, table_name, set, where):
        self.conn.execute(f"UPDATE {table_name} SET {set} WHERE {where}")
        self.conn.commit()

    def delete(self, table_name, where):
        self.conn.execute(f"DELETE FROM {table_name} WHERE {where}")
        self.conn.commit()

    def close(self):
        self.conn.close()

def create_schema(
    database
) -> None:
    database.create_table(
        table_name="mutes",
        columns="user_id INTEGER PRIMARY KEY, guild_id INTEGER, muted BOOL, muted_untill INTEGER"
    )
    database.create_table(
        table_name="roles",
        columns="role_id INTEGER PRIMARY KEY, emoji TEXT, guild_id INTEGER, message_id INTEGER, channel_id INTEGER"
    )

db = Database()
create_schema(db)
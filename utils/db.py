# db.py
import mysql.connector
# from dotenv import load_dotenv
import os

# load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "main-db"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "admin"),
        password=os.getenv("MYSQL_PASSWORD", "admin123"),
        database=os.getenv("MYSQL_DATABASE", "main_db"),
    )
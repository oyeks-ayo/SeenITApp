# test_railway_db.py
import os
import pymysql # type: ignore
from urllib.parse import urlparse

def test_railway_connection():
    # Get the DATABASE_URL from environment (Railway provides this)
    db_url = os.getenv('DATABASE_URL')
    print(f"Database URL: {db_url}")
    
    if not db_url:
        print("❌ DATABASE_URL not found in environment")
        return False
    
    try:
        # Parse the Railway MySQL connection string
        if db_url.startswith('mysql://'):
            # Remove the mysql:// prefix
            connection_string = db_url.replace('mysql://', '')
            
            # Split into user:pass@host:port/database
            if '@' in connection_string:
                user_pass, host_port_db = connection_string.split('@', 1)
                user, password = user_pass.split(':', 1)
                
                # Split host:port/database
                if '/' in host_port_db:
                    host_port, database = host_port_db.split('/', 1)
                    
                    # Split host and port
                    if ':' in host_port:
                        host, port = host_port.split(':', 1)
                    else:
                        host, port = host_port, '3306'
                    
                    print(f"Connecting to: {host}:{port}, database: {database}")
                    
                    # Test the connection
                    connection = pymysql.connect(
                        host=host,
                        port=int(port),
                        user=user,
                        password=password,
                        database=database,
                        connect_timeout=10
                    )
                    
                    print("✅ Successfully connected to Railway MySQL!")
                    connection.close()
                    return True
        
        print("❌ Could not parse DATABASE_URL")
        return False
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_railway_connection()
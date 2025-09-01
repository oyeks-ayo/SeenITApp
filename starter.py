import os
from pkg import app
from pkg.database import check_database_connection

if __name__ == '__main__':
    # Check database connection before starting
    if not check_database_connection(app):
        print("❌ Failed to connect to database. Please check your Railway MySQL plugin.")
        exit(1)
    
    port = int(os.environ.get("PORT", 5000))
    print(f"✅ Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
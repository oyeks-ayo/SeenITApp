import os
from pkg import app

if __name__ == '__main__':
    # app.run(debug=False, port=5000)

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
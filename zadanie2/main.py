from app import createApp, db
from flask import Response
import os
app = createApp() 


@app.route('/loaderio-c96e5336e89edb22b7ec6e9d9f5fd197.txt')
def loaderio_verify():
    return Response("loaderio-c96e5336e89edb22b7ec6e9d9f5fd197", mimetype='text/plain')

with app.app_context():
    if not os.path.exists("instance/sync.db"):
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

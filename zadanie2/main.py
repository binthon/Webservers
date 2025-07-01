from app import createApp, db
import app.model
import os
app = createApp()

with app.app_context():
    if not (os.path.exists("instance/sync.db") and os.path.exists("instance/async.db")):
        db.create_all()  


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

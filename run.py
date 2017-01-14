import temp_hum_api
from flask import Flask
from temp_hum_api.config import configure_app

app = Flask(__name__)
configure_app(app)

if __name__ == '__main__':
    app.run(
        host = app.config['HOST'],
        port = app.config['PORT'],
    )
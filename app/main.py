from flask import Flask
from src.routes import routes
from config import ConfigMongo

app = Flask(__name__)
app.config.from_object(ConfigMongo)
app.register_blueprint(routes)


# main kısmı

if __name__ == '__main__':
    app.run()



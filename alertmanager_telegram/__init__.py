import telegram
from flask import Flask

from alertmanager_telegram.logging import logger


def create_app():
    app = Flask(__name__)
    app.config.from_object("alertmanager_telegram.config")
    token = app.config["TELEGRAM_TOKEN"]

    app.bot = telegram.Bot(token)

    from alertmanager_telegram.messaging import blueprint

    app.register_blueprint(blueprint)

    logger.info("Created app instance")
    return app

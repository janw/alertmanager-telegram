from flask import Blueprint, current_app, jsonify, request

from alertmanager_telegram.logging import logger
from alertmanager_telegram.templating import render

blueprint = Blueprint("messaging", __name__, template_folder="../templates")


@blueprint.route("/alerts", methods=["POST"])
def alerts():
    content = request.get_json()

    if "alerts" not in content or "status" not in content:
        logger.warning("Received invalid request")
        return jsonify(status="invalid"), 400

    alert_count = len(content["alerts"])
    alert_status = content["status"]
    chat_id = current_app.config["TELEGRAM_CHAT_ID"]

    logger.info(f"Received {alert_count} alerts (status={alert_status})")
    try:
        text = render(content)
    except Exception:
        logger.exception("Exception in message rendering")
        return jsonify(status="failed"), 500

    try:
        current_app.bot.send_message(
            chat_id=chat_id,
            parse_mode="HTML",
            disable_web_page_preview=True,
            text=text,
        )
    except Exception:
        logger.exception("Exception during sending message")
        return jsonify(status="failed"), 500

    logger.info("Sent message")
    return jsonify(status="success"), 200
